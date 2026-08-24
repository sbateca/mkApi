from domain.exception.role_exception import RoleNotFoundError
from domain.model.user import User
from domain.spi.user_persistence_port import UserPersistencePort
from infrastructure.output.postgresql.repository.role_repository import (
    RolePostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.user_repository import (
    UserPostgreSQLRepository,
)
from src.infrastructure.output.postgresql.mapper.user_entity_mapper import (
    UserEntityMapper,
)


class UserPersistenceAdapter(UserPersistencePort):
    def __init__(
        self,
        user_repository: UserPostgreSQLRepository,
        user_entity_mapper: UserEntityMapper,
        role_repository: RolePostgreSQLRepository,
    ):
        self.user_repository = user_repository
        self.user_entity_mapper = user_entity_mapper
        self.role_repository = role_repository

    async def save(self, user: User) -> User:
        await self._resolve_roles(user)
        user_entity = self.user_entity_mapper.to_entity(user)
        saved_entity = await self.user_repository.save_user(user_entity)
        return self.user_entity_mapper.to_domain(saved_entity)

    async def find_by_id(self, user_id: str) -> User | None:
        entity = await self.user_repository.get_user_by_id(user_id)
        return self.user_entity_mapper.to_domain(entity) if entity else None

    async def find_all(self) -> list[User]:
        entities = await self.user_repository.get_all_users()
        return [self.user_entity_mapper.to_domain(entity) for entity in entities]

    async def delete(self, user_id: str) -> None:
        await self.user_repository.delete_user(user_id)

    async def update(self, user_id: str, updated_user: User) -> User:
        await self._resolve_roles(updated_user)
        updated_entity = self.user_entity_mapper.to_entity(updated_user)
        saved_entity = await self.user_repository.update_user(user_id, updated_entity)
        return self.user_entity_mapper.to_domain(saved_entity)

    async def find_by_email(self, email: str) -> User | None:
        entity = await self.user_repository.get_user_by_email(email)
        return self.user_entity_mapper.to_domain(entity) if entity else None

    async def find_by_username(self, username: str) -> User | None:
        entity = await self.user_repository.get_user_by_username(username)
        return self.user_entity_mapper.to_domain(entity) if entity else None

    async def _resolve_roles(self, user: User) -> None:
        resolved_roles = []
        for role in user.roles:
            stored_role = await self.role_repository.find_by_name(role.name.value)
            if not stored_role:
                raise RoleNotFoundError()
            resolved_roles.append(
                self.user_entity_mapper.role_entity_mapper.to_domain(stored_role)
            )
        user.roles = resolved_roles
