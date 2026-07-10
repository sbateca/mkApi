from domain.model.test import Test
from domain.spi.test_persistence_port import TestPersistencePort
from infrastructure.output.postgresql.mapper.test_entity_mapper import (
    TestEntityMapper,
)
from infrastructure.output.postgresql.repository.test_repository import (
    TestPostgreSQLRepository,
)


class TestPersistenceAdapter(TestPersistencePort):
    def __init__(
        self,
        repository: TestPostgreSQLRepository,
        entity_mapper: TestEntityMapper,
    ):
        self.repository = repository
        self.entity_mapper = entity_mapper

    async def save_test(self, test: Test) -> Test:
        saved = await self.repository.save_test(self.entity_mapper.to_entity(test))
        return self.entity_mapper.to_domain(saved)

    async def get_tests(self) -> list[Test]:
        return self.entity_mapper.to_domain_list(await self.repository.get_tests())

    async def get_test_by_id(self, test_id: str) -> Test | None:
        entity = await self.repository.get_test_by_id(test_id)
        return self.entity_mapper.to_domain(entity)

    async def update_test(self, test: Test) -> Test:
        updated = await self.repository.update_test(self.entity_mapper.to_entity(test))
        return self.entity_mapper.to_domain(updated)

    async def delete_test(self, test_id: str) -> None:
        await self.repository.delete_test(test_id)
