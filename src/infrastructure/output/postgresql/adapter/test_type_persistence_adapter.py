from domain.model.test_type import TestType
from domain.spi.test_type_persistence_port import TestTypePersistencePort
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper,
)
from infrastructure.output.postgresql.repository.test_type_repository import (
    TestTypePostgreSQLRepository,
)


class TestTypePersistenceAdapter(TestTypePersistencePort):
    def __init__(
        self,
        test_type_repository: TestTypePostgreSQLRepository,
        test_type_entity_mapper: TestTypeEntityMapper,
    ):
        self.test_type_repository = test_type_repository
        self.test_type_entity_mapper = test_type_entity_mapper

    async def get_test_types(self) -> list[TestType]:
        entities = await self.test_type_repository.get_test_types()
        return self.test_type_entity_mapper.to_domain_list(entities)

    async def get_test_type_by_id(self, test_type_id: str) -> TestType | None:
        entity = await self.test_type_repository.get_test_type_by_id(test_type_id)
        return self.test_type_entity_mapper.to_domain(entity) if entity else None

    async def get_test_type_by_name(self, name: str) -> TestType | None:
        entity = await self.test_type_repository.get_test_type_by_name(name)
        return self.test_type_entity_mapper.to_domain(entity) if entity else None

    async def get_test_type_by_name_excluding_id(
        self, name: str, test_type_id: str
    ) -> TestType | None:
        entity = await self.test_type_repository.get_test_type_by_name_excluding_id(
            name, test_type_id
        )
        return self.test_type_entity_mapper.to_domain(entity) if entity else None

    async def save_test_type(self, test_type: TestType) -> TestType:
        entity = self.test_type_entity_mapper.to_entity(test_type)
        saved = await self.test_type_repository.save_test_type(entity)
        return self.test_type_entity_mapper.to_domain(saved)

    async def update_test_type(self, test_type: TestType) -> TestType:
        entity = self.test_type_entity_mapper.to_entity(test_type)
        updated = await self.test_type_repository.update_test_type(entity)
        return self.test_type_entity_mapper.to_domain(updated)

    async def delete_test_type(self, test_type_id: str) -> None:
        await self.test_type_repository.delete_test_type(test_type_id)
