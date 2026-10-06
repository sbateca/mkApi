from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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

    async def get_report_by_id(self, report_id: str) -> ReportEntity | None:
        result = await self.session.execute(
            self._query().where(ReportEntity.id == report_id)
        )
        return result.scalar_one_or_none()

    async def _write(
        self, entity: ReportEntity, test_ids: list, update: bool
    ) -> ReportEntity:
        report_id = entity.id
        try:
            if update:
                await self.session.merge(entity)
                await self.session.execute(
                    delete(report_tests).where(report_tests.c.report_id == report_id)
                )
            else:
                self.session.add(entity)
            await self.session.flush()
            if test_ids:
                await self.session.execute(
                    insert(report_tests),
                    [
                        {
                            "report_id": report_id,
                            "test_id": test_id,
                            "position": position,
                        }
                        for position, test_id in enumerate(test_ids)
                    ],
                )
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return await self.get_report_by_id(str(report_id))

    async def save_report(self, entity: ReportEntity, test_ids: list) -> ReportEntity:
        return await self._write(entity, test_ids, False)

    async def update_report(self, entity: ReportEntity, test_ids: list) -> ReportEntity:
        return await self._write(entity, test_ids, True)

    async def delete_report(self, report_id: str) -> None:
        await self.session.execute(
            delete(ReportEntity).where(ReportEntity.id == report_id)
        )
        await self.session.commit()
