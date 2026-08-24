from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from infrastructure.output.postgresql.entity.user_entity import UserEntity
from infrastructure.output.postgresql.entity.user_role_entity import UserRoleEntity


class UserPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: str):
        result = await self.session.execute(
            select(UserEntity)
            .options(
                selectinload(UserEntity.user_roles).selectinload(UserRoleEntity.role)
            )
            .where(UserEntity.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(
            select(UserEntity)
            .options(
                selectinload(UserEntity.user_roles).selectinload(UserRoleEntity.role)
            )
            .where(UserEntity.username == username)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        result = await self.session.execute(
            select(UserEntity)
            .options(
                selectinload(UserEntity.user_roles).selectinload(UserRoleEntity.role)
            )
            .where(UserEntity.email == email)
        )
        return result.scalar_one_or_none()

    async def save_user(self, user_entity: UserEntity) -> UserEntity:
        self.session.add(user_entity)
        await self.session.commit()
        return await self.get_user_by_id(str(user_entity.id))

    async def update_user(self, user_id: str, user_entity: UserEntity) -> UserEntity:
        current = await self.get_user_by_id(user_id)
        current.name = user_entity.name
        current.username = user_entity.username
        current.password = user_entity.password
        current.email = user_entity.email
        current.user_roles = [
            UserRoleEntity(role_id=user_role.role_id)
            for user_role in user_entity.user_roles
        ]
        await self.session.commit()
        return await self.get_user_by_id(user_id)

    async def get_all_users(self) -> list[UserEntity]:
        result = await self.session.execute(
            select(UserEntity).options(
                selectinload(UserEntity.user_roles).selectinload(UserRoleEntity.role)
            )
        )
        return result.scalars().all()

    async def delete_user(self, user_id: str) -> None:
        user_entity = await self.get_user_by_id(user_id)
        if user_entity:
            await self.session.delete(user_entity)
            await self.session.commit()
