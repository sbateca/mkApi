from domain.model.sample import Sample
from domain.spi.sample_persistence_port import SamplePersistencePort
from infrastructure.output.postgresql.mapper.sample_entity_mapper import (
    SampleEntityMapper,
)
from infrastructure.output.postgresql.repository.sample_repository import (
    SamplePostgreSQLRepository,
)


class SamplePersistenceAdapter(SamplePersistencePort):
    def __init__(
        self,
        repository: SamplePostgreSQLRepository,
        entity_mapper: SampleEntityMapper,
    ):
        self.repository = repository
        self.entity_mapper = entity_mapper

    async def save_sample(self, sample: Sample) -> Sample:
        saved = await self.repository.save_sample(self.entity_mapper.to_entity(sample))
        return self.entity_mapper.to_domain(saved)

    async def get_samples(self) -> list[Sample]:
        return self.entity_mapper.to_domain_list(await self.repository.get_samples())

    async def get_sample_by_id(self, sample_id: str) -> Sample | None:
        entity = await self.repository.get_sample_by_id(sample_id)
        return self.entity_mapper.to_domain(entity)

    async def get_sample_by_sample_code(self, sample_code: str) -> Sample | None:
        entity = await self.repository.get_sample_by_sample_code(sample_code)
        return self.entity_mapper.to_domain(entity)

    async def get_sample_by_sample_code_excluding_id(
        self, sample_code: str, sample_id: str
    ) -> Sample | None:
        entity = await self.repository.get_sample_by_sample_code_excluding_id(
            sample_code, sample_id
        )
        return self.entity_mapper.to_domain(entity)

    async def update_sample(self, sample: Sample) -> Sample:
        updated = await self.repository.update_sample(
            self.entity_mapper.to_entity(sample)
        )
        return self.entity_mapper.to_domain(updated)

    async def delete_sample(self, sample_id: str) -> None:
        await self.repository.delete_sample(sample_id)
