from domain.model.sample_type import SampleType
from domain.spi.sample_type_persistence_port import SampleTypePersistencePort
from infrastructure.output.postgresql.mapper.sample_type_entity_mapper import (
    SampleTypeEntityMapper,
)
from infrastructure.output.postgresql.repository.sample_type_repository import (
    SampleTypePostgreSQLRepository,
)


class SampleTypePersistenceAdapter(SampleTypePersistencePort):
    def __init__(
        self,
        repository: SampleTypePostgreSQLRepository,
        entity_mapper: SampleTypeEntityMapper,
    ):
        self.repository = repository
        self.entity_mapper = entity_mapper

    async def get_sample_types(self) -> list[SampleType]:
        return self.entity_mapper.to_domain_list(
            await self.repository.get_sample_types()
        )

    async def get_sample_type_by_id(self, sample_type_id: str) -> SampleType | None:
        entity = await self.repository.get_sample_type_by_id(sample_type_id)
        return self.entity_mapper.to_domain(entity) if entity else None

    async def get_sample_type_by_name(self, name: str) -> SampleType | None:
        entity = await self.repository.get_sample_type_by_name(name)
        return self.entity_mapper.to_domain(entity) if entity else None

    async def get_sample_type_by_name_excluding_id(
        self, name: str, sample_type_id: str
    ) -> SampleType | None:
        entity = await self.repository.get_sample_type_by_name_excluding_id(
            name, sample_type_id
        )
        return self.entity_mapper.to_domain(entity) if entity else None

    async def save_sample_type(self, sample_type: SampleType) -> SampleType:
        saved = await self.repository.save_sample_type(
            self.entity_mapper.to_entity(sample_type)
        )
        return self.entity_mapper.to_domain(saved)

    async def update_sample_type(self, sample_type: SampleType) -> SampleType:
        updated = await self.repository.update_sample_type(
            self.entity_mapper.to_entity(sample_type)
        )
        return self.entity_mapper.to_domain(updated)

    async def delete_sample_type(self, sample_type_id: str) -> None:
        await self.repository.delete_sample_type(sample_type_id)
