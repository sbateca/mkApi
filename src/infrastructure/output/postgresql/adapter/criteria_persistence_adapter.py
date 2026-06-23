from domain.model.criteria import Criteria
from domain.spi.criteria_persistence_port import CriteriaPersistencePort
from infrastructure.output.postgresql.mapper.criteria_entity_mapper import (
    CriteriaEntityMapper,
)
from infrastructure.output.postgresql.repository.criteria_repository import (
    CriteriaPostgreSQLRepository,
)


class CriteriaPersistenceAdapter(CriteriaPersistencePort):
    def __init__(
        self,
        repository: CriteriaPostgreSQLRepository,
        entity_mapper: CriteriaEntityMapper,
    ):
        self.repository = repository
        self.entity_mapper = entity_mapper

    async def get_criteria(self) -> list[Criteria]:
        return self.entity_mapper.to_domain_list(await self.repository.get_criteria())

    async def get_criteria_by_id(self, criteria_id: str) -> Criteria | None:
        entity = await self.repository.get_criteria_by_id(criteria_id)
        return self.entity_mapper.to_domain(entity) if entity else None

    async def get_criteria_by_name(self, name: str) -> Criteria | None:
        entity = await self.repository.get_criteria_by_name(name)
        return self.entity_mapper.to_domain(entity) if entity else None

    async def get_criteria_by_name_excluding_id(
        self, name: str, criteria_id: str
    ) -> Criteria | None:
        entity = await self.repository.get_criteria_by_name_excluding_id(
            name, criteria_id
        )
        return self.entity_mapper.to_domain(entity) if entity else None

    async def save_criteria(self, criteria: Criteria) -> Criteria:
        saved = await self.repository.save_criteria(
            self.entity_mapper.to_entity(criteria)
        )
        return self.entity_mapper.to_domain(saved)

    async def update_criteria(self, criteria: Criteria) -> Criteria:
        updated = await self.repository.update_criteria(
            self.entity_mapper.to_entity(criteria)
        )
        return self.entity_mapper.to_domain(updated)

    async def delete_criteria(self, criteria_id: str) -> None:
        await self.repository.delete_criteria(criteria_id)
