from domain.model.role import Role
from domain.util.constants import UserRole
from infrastructure.output.postgresql.entity.role_entity import RoleEntity


class RoleEntityMapper:
    def __init__(self):
        pass

    def to_entity(self, role: Role) -> RoleEntity:
        return RoleEntity(id=role.id, name=role.name.value)

    def to_domain(self, entity: RoleEntity) -> Role:
        return Role(id=entity.id, name=UserRole(entity.name))

    def to_domain_list(self, entities: list[RoleEntity]) -> list[Role]:
        return [self.to_domain(entity) for entity in entities]
