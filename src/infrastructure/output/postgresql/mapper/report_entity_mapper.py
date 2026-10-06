from domain.model.report import Report
from infrastructure.output.postgresql.entity.report_entity import ReportEntity
from infrastructure.output.postgresql.mapper.sample_entity_mapper import (
    SampleEntityMapper,
)
from infrastructure.output.postgresql.mapper.test_entity_mapper import TestEntityMapper


class ReportEntityMapper:
    def __init__(
        self,
        sample_entity_mapper: SampleEntityMapper,
        test_entity_mapper: TestEntityMapper,
    ):
        self.sample_entity_mapper = sample_entity_mapper
        self.test_entity_mapper = test_entity_mapper

    def to_entity(self, report: Report) -> ReportEntity:
        return ReportEntity(
            id=report.id,
            report_number=report.report_number,
            report_date=report.report_date,
            status=report.status,
            sample_id=report.sample.id,
        )

    def to_domain(self, entity: ReportEntity) -> Report | None:
        if entity is None:
            return None
        return Report(
            id=entity.id,
            report_number=entity.report_number,
            report_date=entity.report_date,
            status=entity.status,
            sample=self.sample_entity_mapper.to_domain(entity.sample),
            tests=self.test_entity_mapper.to_domain_list(entity.tests),
        )

    def to_domain_list(self, entities: list[ReportEntity]) -> list[Report]:
        return [self.to_domain(entity) for entity in entities]
