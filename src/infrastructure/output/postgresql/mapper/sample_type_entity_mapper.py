from domain.model.sample_type import SampleType
from infrastructure.output.postgresql.entity.sample_type_entity import (
    SampleTypeEntity,
)


class SampleTypeEntityMapper:
    def to_entity(self, sample_type: SampleType) -> SampleTypeEntity:
        return SampleTypeEntity(id=sample_type.id, name=sample_type.name)

    def to_domain(self, entity: SampleTypeEntity) -> SampleType:
        return SampleType(id=entity.id, name=entity.name)

    def to_domain_list(self, entities: list[SampleTypeEntity]) -> list[SampleType]:
        return [self.to_domain(entity) for entity in entities]
