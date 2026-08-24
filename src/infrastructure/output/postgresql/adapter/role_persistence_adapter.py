from domain.model.role import Role
from domain.spi.role_persistence_port import RolePersistencePort
from infrastructure.output.postgresql.mapper.role_entity_mapper import RoleEntityMapper
from infrastructure.output.postgresql.repository.role_repository import (
    RolePostgreSQLRepository,
)


class RolePersistenceAdapter(RolePersistencePort):
    def __init__(
        self,
        role_repository: RolePostgreSQLRepository,
        role_entity_mapper: RoleEntityMapper,
    ):
        self.role_repository = role_repository
        self.role_entity_mapper = role_entity_mapper

    async def save(self, role: Role):
        role_entity = self.role_entity_mapper.to_entity(role)
        saved_entity = await self.role_repository.save(role_entity)
        return self.role_entity_mapper.to_domain(saved_entity)

    async def find_by_id(self, role_id: str):
        entity = await self.role_repository.find_by_id(role_id)
        return self.role_entity_mapper.to_domain(entity) if entity else None

    async def find_all(self):
        entities = await self.role_repository.find_all()
        return self.role_entity_mapper.to_domain_list(entities)

    async def delete(self, role_id: str):
        await self.role_repository.delete(role_id)

    async def update(self, role_id: str, updated_role: Role):
        updated_entity = self.role_entity_mapper.to_entity(updated_role)
        saved_entity = await self.role_repository.update(role_id, updated_entity)
        return self.role_entity_mapper.to_domain(saved_entity)

    async def find_by_name(self, name: str):
        entity = await self.role_repository.find_by_name(name)
        return self.role_entity_mapper.to_domain(entity) if entity else None

    async def find_roles_by_names(self, role_names: list[str]):
        entities = await self.role_repository.find_roles_by_names(role_names)
        return self.role_entity_mapper.to_domain_list(entities)
