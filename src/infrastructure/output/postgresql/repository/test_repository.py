from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_expression

from domain.exception.test_exception import LinkedReportTestError, TestNotFoundError
from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity
from infrastructure.output.postgresql.entity.report_entity import report_tests
from infrastructure.output.postgresql.entity.test_entity import TestEntity


class TestPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _linked_to_report():
        return (
            select(report_tests.c.test_id)
            .where(report_tests.c.test_id == TestEntity.id)
            .exists()
        )

    async def get_tests(self) -> list[TestEntity]:
        result = await self.session.execute(
            select(TestEntity)
            .options(
                with_expression(TestEntity.report_linked, self._linked_to_report()),
                selectinload(TestEntity.test_type),
                selectinload(TestEntity.analyte).selectinload(AnalyteEntity.test_type),
                selectinload(TestEntity.analysis_method),
                selectinload(TestEntity.criteria),
            )
            .order_by(TestEntity.sample_id)
        )
        return result.scalars().all()

    async def get_test_by_id(self, test_id: str) -> TestEntity | None:
        result = await self.session.execute(
            select(TestEntity)
            .options(
                with_expression(TestEntity.report_linked, self._linked_to_report()),
                selectinload(TestEntity.test_type),
                selectinload(TestEntity.analyte).selectinload(AnalyteEntity.test_type),
                selectinload(TestEntity.analysis_method),
                selectinload(TestEntity.criteria),
            )
            .where(TestEntity.id == test_id)
        )
        return result.scalar_one_or_none()

    async def save_test(self, entity: TestEntity) -> TestEntity:
        self.session.add(entity)
        await self.session.commit()
        return await self.get_test_by_id(str(entity.id))

    async def update_test(self, entity: TestEntity) -> TestEntity:
        await self._write_unlinked_test(
            update(TestEntity)
            .where(TestEntity.id == entity.id)
            .values(
                sample_id=entity.sample_id,
                test_type_id=entity.test_type_id,
                analyte_id=entity.analyte_id,
                analysis_method_id=entity.analysis_method_id,
                criteria_id=entity.criteria_id,
                result=entity.result,
            ),
            entity.id,
        )
        return await self.get_test_by_id(str(entity.id))

    async def delete_test(self, test_id: str) -> None:
        await self._write_unlinked_test(
            delete(TestEntity).where(TestEntity.id == test_id), test_id
        )

    async def _write_unlinked_test(self, statement, test_id) -> None:
        try:
            result = await self.session.execute(
                statement.where(~self._linked_to_report()).returning(TestEntity.id)
            )
            if result.scalar_one_or_none() is None:
                existing = await self.session.execute(
                    select(TestEntity.id).where(TestEntity.id == test_id)
                )
                if existing.scalar_one_or_none() is None:
                    raise TestNotFoundError()
                raise LinkedReportTestError()
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
