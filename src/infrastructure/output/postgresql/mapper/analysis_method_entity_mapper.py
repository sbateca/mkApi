from domain.model.analysis_method import AnalysisMethod
from infrastructure.output.postgresql.entity.analysis_method_entity import (
    AnalysisMethodEntity,
)


class AnalysisMethodEntityMapper:
    def to_entity(self, analysis_method: AnalysisMethod) -> AnalysisMethodEntity:
        return AnalysisMethodEntity(
            id=analysis_method.id,
            name=analysis_method.name,
        )

    def to_domain(self, entity: AnalysisMethodEntity) -> AnalysisMethod:
        return AnalysisMethod(id=entity.id, name=entity.name)

    def to_domain_list(
        self, entities: list[AnalysisMethodEntity]
    ) -> list[AnalysisMethod]:
        return [self.to_domain(entity) for entity in entities]
