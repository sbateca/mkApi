from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from domain.spi.report_test_persistence_port import ReportTestPersistencePort
from infrastructure.output.postgresql.entity.report_entity import report_tests


class ReportTestPersistenceAdapter(ReportTestPersistencePort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_report_tests(
        self, report_id: UUID, test_ids: Sequence[UUID]
    ) -> None:
        if test_ids:
            await self.session.execute(
                insert(report_tests),
                [
                    {"report_id": report_id, "test_id": test_id, "position": position}
                    for position, test_id in enumerate(test_ids)
                ],
            )
