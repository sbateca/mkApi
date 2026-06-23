from domain.model.criteria import Criteria
from infrastructure.output.postgresql.entity.criteria_entity import CriteriaEntity


class CriteriaEntityMapper:
    def to_entity(self, criteria: Criteria) -> CriteriaEntity:
        return CriteriaEntity(id=criteria.id, name=criteria.name)

    def to_domain(self, entity: CriteriaEntity) -> Criteria:
        return Criteria(id=entity.id, name=entity.name)

    def to_domain_list(self, entities: list[CriteriaEntity]) -> list[Criteria]:
        return [self.to_domain(entity) for entity in entities]
