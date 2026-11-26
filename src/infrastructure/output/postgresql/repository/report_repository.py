from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.exception.domain_exception import DomainError
from domain.exception.report_exception import (
    ReportActionDeniedError,
    ReportNotFoundError,
    ReportSampleConsistencyError,
)
from domain.exception.test_exception import LinkedReportTestError
from domain.spi.report_test_persistence_port import ReportTestPersistencePort
from domain.util.constants import (
    REPORT_NOT_DRAFT_ERROR_MESSAGE,
    REPORT_TEST_ID_ALREADY_EXISTS_ERROR_MESSAGE,
    ActionDecisionCode,
    ReportStatus,
)
from infrastructure.output.postgresql.adapter.report_test_persistence_adapter import (
    ReportTestPersistenceAdapter,
)
from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity
from infrastructure.output.postgresql.entity.report_entity import (
    ReportEntity,
    report_tests,
)
from infrastructure.output.postgresql.entity.sample_entity import SampleEntity
from infrastructure.output.postgresql.entity.test_entity import TestEntity


class ReportPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _query(self):
        return (
            select(ReportEntity)
            .options(
                selectinload(ReportEntity.sample).selectinload(
                    SampleEntity.sample_type
                ),
                selectinload(ReportEntity.sample).selectinload(SampleEntity.client),
                selectinload(ReportEntity.tests).selectinload(TestEntity.test_type),
                selectinload(ReportEntity.tests)
                .selectinload(TestEntity.analyte)
                .selectinload(AnalyteEntity.test_type),
                selectinload(ReportEntity.tests).selectinload(
                    TestEntity.analysis_method
                ),
                selectinload(ReportEntity.tests).selectinload(TestEntity.criteria),
            )
            .execution_options(populate_existing=True)
        )

    async def get_reports(self) -> list[ReportEntity]:
        result = await self.session.execute(
            self._query().order_by(ReportEntity.report_date, ReportEntity.id)
        )
        return result.scalars().all()

    async def get_reports_by_client_id(self, client_id: UUID) -> list[ReportEntity]:
        result = await self.session.execute(
            self._query()
            .join(ReportEntity.sample)
            .where(SampleEntity.client_id == client_id)
            .order_by(ReportEntity.report_date, ReportEntity.id)
        )
        return result.scalars().all()

    async def get_report_by_id(self, report_id: str) -> ReportEntity | None:
        result = await self.session.execute(
            self._query().where(ReportEntity.id == report_id)
        )
        return result.scalar_one_or_none()

    async def _write(
        self,
        entity: ReportEntity,
        tests: list[TestEntity],
        replace: bool,
        report_tests_port: ReportTestPersistencePort | None = None,
    ) -> ReportEntity:
        report_id = entity.id
        previous_ids: set[UUID] = set()
        try:
            if replace:
                result = await self.session.execute(
                    update(ReportEntity)
                    .where(
                        ReportEntity.id == report_id,
                        self._draft_status(),
                    )
                    .values(
                        report_number=entity.report_number,
                        report_date=entity.report_date,
                        sample_id=entity.sample_id,
                    )
                    .returning(ReportEntity.id)
                )
                if result.scalar_one_or_none() is None:
                    await self._raise_draft_write_error(report_id)
                previous_ids = await self._remove_test_links(report_id)
            else:
                self.session.add(entity)
            await self.session.flush()
            report_id = entity.id
            test_ids = [test.id for test in tests]
            await self._update_retained_tests(
                [test for test in tests if test.id in previous_ids], entity.sample_id
            )
            await self._insert_tests(
                [test for test in tests if test.id not in previous_ids]
            )
            await self._delete_unlinked_tests(previous_ids.difference(test_ids))
            if test_ids:
                links = report_tests_port or ReportTestPersistenceAdapter(self.session)
                await links.save_report_tests(report_id, test_ids)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return await self.get_report_by_id(str(report_id))

    async def save_report(
        self,
        entity: ReportEntity,
        tests: list[TestEntity],
        *,
        report_tests_port: ReportTestPersistencePort | None = None,
    ) -> ReportEntity:
        return await self._write(entity, tests, False, report_tests_port)

    async def update_report(
        self, entity: ReportEntity, tests: list[TestEntity]
    ) -> ReportEntity:
        return await self._write(entity, tests, True)

    async def update_report_status(self, report_id: str, status: str) -> ReportEntity:
        try:
            result = await self.session.execute(
                select(ReportEntity.sample_id)
                .where(ReportEntity.id == report_id, self._draft_status())
                .with_for_update()
            )
            sample_id = result.scalar_one_or_none()
            if sample_id is None:
                await self._raise_draft_write_error(report_id)
            # Serialize approval with client changes on the sample.
            await self.session.execute(
                select(SampleEntity.id)
                .where(SampleEntity.id == sample_id)
                .with_for_update(key_share=True)
            )
            await self.session.execute(
                update(ReportEntity)
                .where(ReportEntity.id == report_id)
                .values(status=status)
            )
            report = await self.get_report_by_id(report_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return report

    async def delete_report(self, report_id: str) -> None:
        try:
            result = await self.session.execute(
                select(ReportEntity.id)
                .where(ReportEntity.id == report_id, self._draft_status())
                .with_for_update()
            )
            if result.scalar_one_or_none() is None:
                await self._raise_draft_write_error(report_id)
            await self._delete_unlinked_tests(await self._remove_test_links(report_id))
            await self.session.execute(
                delete(ReportEntity).where(ReportEntity.id == report_id)
            )
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def _remove_test_links(self, report_id: str | UUID) -> set[UUID]:
        result = await self.session.execute(
            delete(report_tests)
            .where(report_tests.c.report_id == report_id)
            .returning(report_tests.c.test_id)
        )
        return set(result.scalars())

    async def _update_retained_tests(
        self, tests: list[TestEntity], sample_id: UUID
    ) -> None:
        for test in tests:
            linked = select(report_tests.c.test_id).where(
                report_tests.c.test_id == TestEntity.id
            )
            result = await self.session.execute(
                select(TestEntity.sample_id, linked.exists())
                .where(TestEntity.id == test.id)
                .with_for_update()
            )
            current_sample_id, linked_elsewhere = result.one()
            if current_sample_id != sample_id:
                raise ReportSampleConsistencyError()
            if linked_elsewhere:
                raise LinkedReportTestError()
            await self.session.execute(
                update(TestEntity)
                .where(TestEntity.id == test.id)
                .values(**self._test_values(test))
            )

    @staticmethod
    def _test_values(test: TestEntity) -> dict:
        return {
            "sample_id": test.sample_id,
            "test_type_id": test.test_type_id,
            "analyte_id": test.analyte_id,
            "analysis_method_id": test.analysis_method_id,
            "criteria_id": test.criteria_id,
            "result": test.result,
        }

    async def _insert_tests(self, tests: list[TestEntity]) -> None:
        if tests:
            rows = [{"id": test.id, **self._test_values(test)} for test in tests]
            result = await self.session.execute(
                insert(TestEntity)
                .on_conflict_do_nothing(index_elements=[TestEntity.id])
                .returning(TestEntity.id),
                rows,
            )
            if set(result.scalars()) != {test.id for test in tests}:
                raise DomainError(REPORT_TEST_ID_ALREADY_EXISTS_ERROR_MESSAGE)

    async def _delete_unlinked_tests(self, test_ids: set[UUID]) -> None:
        if test_ids:
            await self.session.execute(
                delete(TestEntity).where(
                    TestEntity.id.in_(test_ids),
                    ~select(report_tests.c.test_id)
                    .where(report_tests.c.test_id == TestEntity.id)
                    .exists(),
                )
            )

    @staticmethod
    def _draft_status():
        return func.lower(ReportEntity.status) == ReportStatus.DRAFT.value.lower()

    async def _raise_draft_write_error(self, report_id: str | UUID) -> None:
        result = await self.session.execute(
            select(ReportEntity.id).where(ReportEntity.id == report_id)
        )
        if result.scalar_one_or_none() is None:
            raise ReportNotFoundError()
        raise ReportActionDeniedError(
            ActionDecisionCode.REPORT_NOT_DRAFT.value, REPORT_NOT_DRAFT_ERROR_MESSAGE
        )
