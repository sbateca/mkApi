from domain.model.test_type import TestType
from infrastructure.output.postgresql.entity.test_type_entity import TestTypeEntity


class TestTypeEntityMapper:
    def to_entity(self, test_type: TestType) -> TestTypeEntity:
        return TestTypeEntity(id=test_type.id, name=test_type.name)

    def to_domain(self, entity: TestTypeEntity) -> TestType:
        return TestType(id=entity.id, name=entity.name)

    def to_domain_list(self, entities: list[TestTypeEntity]) -> list[TestType]:
        return [self.to_domain(entity) for entity in entities]
