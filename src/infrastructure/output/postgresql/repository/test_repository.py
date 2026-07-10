from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity
from infrastructure.output.postgresql.entity.test_entity import TestEntity


class TestPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tests(self) -> list[TestEntity]:
        result = await self.session.execute(
            select(TestEntity)
            .options(
                selectinload(TestEntity.test_type),
                selectinload(TestEntity.analyte).selectinload(AnalyteEntity.test_type),
                selectinload(TestEntity.analysis_method),
                selectinload(TestEntity.criteria),
            )
            .order_by(TestEntity.sample_id)
        )
        return result.scalars().all()

    async def get_test_by_id(self, test_id: str) -> TestEntity | None:
        result = await self.session.execute(
            select(TestEntity)
            .options(
                selectinload(TestEntity.test_type),
                selectinload(TestEntity.analyte).selectinload(AnalyteEntity.test_type),
                selectinload(TestEntity.analysis_method),
                selectinload(TestEntity.criteria),
            )
            .where(TestEntity.id == test_id)
        )
        return result.scalar_one_or_none()

    async def save_test(self, entity: TestEntity) -> TestEntity:
        self.session.add(entity)
        await self.session.commit()
        return await self.get_test_by_id(str(entity.id))

    async def update_test(self, entity: TestEntity) -> TestEntity:
        merged = await self.session.merge(entity)
        await self.session.commit()
        return await self.get_test_by_id(str(merged.id))

    async def delete_test(self, test_id: str) -> None:
        await self.session.execute(delete(TestEntity).where(TestEntity.id == test_id))
        await self.session.commit()
