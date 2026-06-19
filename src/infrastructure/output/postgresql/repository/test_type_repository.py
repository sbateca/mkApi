from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.test_type_entity import TestTypeEntity


class TestTypePostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_test_types(self) -> list[TestTypeEntity]:
        result = await self.session.execute(
            select(TestTypeEntity).order_by(TestTypeEntity.name)
        )
        return result.scalars().all()

    async def get_test_type_by_id(self, test_type_id: str) -> TestTypeEntity | None:
        result = await self.session.execute(
            select(TestTypeEntity).where(TestTypeEntity.id == test_type_id)
        )
        return result.scalar_one_or_none()

    async def get_test_type_by_name(self, name: str) -> TestTypeEntity | None:
        result = await self.session.execute(
            select(TestTypeEntity).where(TestTypeEntity.name == name)
        )
        return result.scalar_one_or_none()

    async def get_test_type_by_name_excluding_id(
        self, name: str, test_type_id: str
    ) -> TestTypeEntity | None:
        result = await self.session.execute(
            select(TestTypeEntity).where(
                (TestTypeEntity.name == name) & (TestTypeEntity.id != test_type_id)
            )
        )
        return result.scalar_one_or_none()

    async def save_test_type(self, entity: TestTypeEntity) -> TestTypeEntity:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update_test_type(self, entity: TestTypeEntity) -> TestTypeEntity:
        merged = await self.session.merge(entity)
        await self.session.commit()
        await self.session.refresh(merged)
        return merged

    async def delete_test_type(self, test_type_id: str) -> None:
        await self.session.execute(
            delete(TestTypeEntity).where(TestTypeEntity.id == test_type_id)
        )
        await self.session.commit()
