from domain.model.report import Report
from domain.spi.report_persistence_port import ReportPersistencePort
from infrastructure.output.postgresql.mapper.report_entity_mapper import (
    ReportEntityMapper,
)
from infrastructure.output.postgresql.repository.report_repository import (
    ReportPostgreSQLRepository,
)


class ReportPersistenceAdapter(ReportPersistencePort):
    def __init__(
        self,
        repository: ReportPostgreSQLRepository,
        entity_mapper: ReportEntityMapper,
    ):
        self.repository = repository
        self.entity_mapper = entity_mapper

    async def save_report(self, report: Report) -> Report:
        saved = await self.repository.save_report(
            self.entity_mapper.to_entity(report), [test.id for test in report.tests]
        )
        return self.entity_mapper.to_domain(saved)

    async def get_reports(self) -> list[Report]:
        return self.entity_mapper.to_domain_list(await self.repository.get_reports())

    async def get_report_by_id(self, report_id: str) -> Report | None:
        entity = await self.repository.get_report_by_id(report_id)
        return self.entity_mapper.to_domain(entity)

    async def update_report(self, report: Report) -> Report:
        updated = await self.repository.update_report(
            self.entity_mapper.to_entity(report), [test.id for test in report.tests]
        )
        return self.entity_mapper.to_domain(updated)

    async def delete_report(self, report_id: str) -> None:
        await self.repository.delete_report(report_id)
