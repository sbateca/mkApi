from domain.model.analysis_method import AnalysisMethod
from domain.spi.analysis_method_persistence_port import AnalysisMethodPersistencePort
from infrastructure.output.postgresql.mapper.analysis_method_entity_mapper import (
    AnalysisMethodEntityMapper,
)
from infrastructure.output.postgresql.repository.analysis_method_repository import (
    AnalysisMethodPostgreSQLRepository,
)


class AnalysisMethodPersistenceAdapter(AnalysisMethodPersistencePort):
    def __init__(
        self,
        analysis_method_repository: AnalysisMethodPostgreSQLRepository,
        analysis_method_entity_mapper: AnalysisMethodEntityMapper,
    ):
        self.analysis_method_repository = analysis_method_repository
        self.analysis_method_entity_mapper = analysis_method_entity_mapper

    async def get_analysis_methods(self) -> list[AnalysisMethod]:
        entities = await self.analysis_method_repository.get_analysis_methods()
        return self.analysis_method_entity_mapper.to_domain_list(entities)

    async def get_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod | None:
        entity = await self.analysis_method_repository.get_analysis_method_by_id(
            analysis_method_id
        )
        return self.analysis_method_entity_mapper.to_domain(entity) if entity else None

    async def get_analysis_method_by_name(self, name: str) -> AnalysisMethod | None:
        entity = await self.analysis_method_repository.get_analysis_method_by_name(name)
        return self.analysis_method_entity_mapper.to_domain(entity) if entity else None

    async def get_analysis_method_by_name_excluding_id(
        self, name: str, analysis_method_id: str
    ) -> AnalysisMethod | None:
        entity = await self.analysis_method_repository.get_analysis_method_by_name_excluding_id(
            name, analysis_method_id
        )
        return self.analysis_method_entity_mapper.to_domain(entity) if entity else None

    async def save_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        entity = self.analysis_method_entity_mapper.to_entity(analysis_method)
        saved = await self.analysis_method_repository.save_analysis_method(entity)
        return self.analysis_method_entity_mapper.to_domain(saved)

    async def update_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        entity = self.analysis_method_entity_mapper.to_entity(analysis_method)
        updated = await self.analysis_method_repository.update_analysis_method(entity)
        return self.analysis_method_entity_mapper.to_domain(updated)

    async def delete_analysis_method(self, analysis_method_id: str) -> None:
        await self.analysis_method_repository.delete_analysis_method(analysis_method_id)
