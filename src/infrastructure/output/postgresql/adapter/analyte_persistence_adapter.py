from domain.model.analyte import Analyte
from domain.spi.analyte_persistence_port import AnalytePersistencePort
from infrastructure.output.postgresql.mapper.analyte_entity_mapper import (
    AnalyteEntityMapper,
)
from infrastructure.output.postgresql.repository.analyte_repository import (
    AnalytePostgreSQLRepository,
)


class AnalytePersistenceAdapter(AnalytePersistencePort):
    def __init__(
        self,
        analyte_repository: AnalytePostgreSQLRepository,
        analyte_entity_mapper: AnalyteEntityMapper,
    ):
        self.analyte_repository = analyte_repository
        self.analyte_entity_mapper = analyte_entity_mapper

    async def save_analyte(self, analyte: Analyte) -> Analyte:
        analyte_entity = self.analyte_entity_mapper.to_entity(analyte)
        saved_analyte_entity = await self.analyte_repository.save_analyte(
            analyte_entity
        )
        return self.analyte_entity_mapper.to_domain(saved_analyte_entity)

    async def get_analytes(self) -> list[Analyte]:
        analytes = await self.analyte_repository.get_analytes()
        return self.analyte_entity_mapper.to_domain_list(analytes)

    async def get_analyte_by_id(self, analyte_id: str) -> Analyte | None:
        analyte_entity = await self.analyte_repository.get_analyte_by_id(analyte_id)
        return self.analyte_entity_mapper.to_domain(analyte_entity)

    async def get_analyte_by_name(self, name: str) -> Analyte | None:
        analyte_entity = await self.analyte_repository.get_analyte_by_name(name)
        return self.analyte_entity_mapper.to_domain(analyte_entity)

    async def get_analyte_by_name_excluding_id(
        self, name: str, analyte_id: str
    ) -> Analyte | None:
        analyte_entity = await self.analyte_repository.get_analyte_by_name_excluding_id(
            name, analyte_id
        )
        return self.analyte_entity_mapper.to_domain(analyte_entity)

    async def update_analyte(self, analyte: Analyte) -> Analyte:
        analyte_entity = self.analyte_entity_mapper.to_entity(analyte)
        updated_analyte = await self.analyte_repository.update_analyte(analyte_entity)
        return self.analyte_entity_mapper.to_domain(updated_analyte)

    async def delete_analyte(self, analyte_id: str) -> None:
        await self.analyte_repository.delete_analyte(analyte_id)
