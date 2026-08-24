from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.role_entity import RoleEntity


class RolePostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, role_entity):
        self.session.add(role_entity)
        await self.session.commit()
        await self.session.refresh(role_entity)
        return role_entity

    async def find_by_id(self, role_id: str):
        result = await self.session.execute(
            select(RoleEntity).where(RoleEntity.id == role_id)
        )
        return result.scalar_one_or_none()

    async def find_all(self):
        result = await self.session.execute(select(RoleEntity))
        return result.scalars().all()

    async def delete(self, role_id: str):
        role_entity = await self.find_by_id(role_id)
        if role_entity:
            await self.session.delete(role_entity)
            await self.session.commit()

    async def update(self, role_id: str, updated_role_entity):
        existing_role_entity = await self.find_by_id(role_id)
        if existing_role_entity:
            existing_role_entity.name = updated_role_entity.name
            await self.session.commit()
            await self.session.refresh(existing_role_entity)
            return existing_role_entity
        return None

    async def find_by_name(self, name: str):
        result = await self.session.execute(
            select(RoleEntity).where(RoleEntity.name == name)
        )
        return result.scalar_one_or_none()

    async def find_roles_by_names(self, role_names: list[str]):
        result = await self.session.execute(
            select(RoleEntity).where(RoleEntity.name.in_(role_names))
        )
        return result.scalars().all()
