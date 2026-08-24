from domain.model.user import User
from infrastructure.output.postgresql.entity.user_entity import UserEntity
from infrastructure.output.postgresql.entity.user_role_entity import UserRoleEntity
from infrastructure.output.postgresql.mapper.role_entity_mapper import RoleEntityMapper


class UserEntityMapper:
    def __init__(self, role_entity_mapper: RoleEntityMapper):
        self.role_entity_mapper = role_entity_mapper

    def to_entity(self, user: User) -> UserEntity:
        entity = UserEntity(
            id=user.id,
            name=user.name,
            username=user.username,
            password=user.password,
            email=user.email,
        )
        entity.user_roles = [UserRoleEntity(role_id=role.id) for role in user.roles]
        return entity

    def to_domain(self, entity: UserEntity) -> User:
        return User(
            id=entity.id,
            name=entity.name,
            username=entity.username,
            password=entity.password,
            email=entity.email,
            roles=[
                self.role_entity_mapper.to_domain(user_role.role)
                for user_role in entity.user_roles
            ],
        )
