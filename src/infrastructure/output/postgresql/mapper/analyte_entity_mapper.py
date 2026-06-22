from domain.model.analyte import Analyte
from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper,
)


class AnalyteEntityMapper:
    def __init__(self, test_type_entity_mapper: TestTypeEntityMapper):
        self.test_type_entity_mapper = test_type_entity_mapper

    def to_entity(self, analyte: Analyte) -> AnalyteEntity:
        return AnalyteEntity(
            id=analyte.id, name=analyte.name, test_type_id=analyte.test_type.id
        )

    def to_domain(self, analyte_entity: AnalyteEntity) -> Analyte | None:
        if analyte_entity:
            test_type = self.test_type_entity_mapper.to_domain(analyte_entity.test_type)
            return Analyte(
                id=analyte_entity.id, name=analyte_entity.name, test_type=test_type
            )
        return None

    def to_domain_list(self, analyte_entities: list[AnalyteEntity]) -> list[Analyte]:
        return [self.to_domain(entity) for entity in analyte_entities]
