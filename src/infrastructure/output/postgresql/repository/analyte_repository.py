from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity


class AnalytePostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_analytes(self) -> list[AnalyteEntity]:
        result = await self.session.execute(
            select(AnalyteEntity)
            .options(selectinload(AnalyteEntity.test_type))
            .order_by(AnalyteEntity.name)
        )
        return result.scalars().all()

    async def get_analyte_by_id(self, analyte_id: str) -> AnalyteEntity | None:
        result = await self.session.execute(
            select(AnalyteEntity)
            .options(selectinload(AnalyteEntity.test_type))
            .where(AnalyteEntity.id == analyte_id)
        )
        return result.scalar_one_or_none()

    async def get_analyte_by_name(self, name: str) -> AnalyteEntity | None:
        result = await self.session.execute(
            select(AnalyteEntity)
            .options(selectinload(AnalyteEntity.test_type))
            .where(AnalyteEntity.name == name)
        )
        return result.scalar_one_or_none()

    async def get_analyte_by_name_excluding_id(
        self, name: str, analyte_id: str
    ) -> AnalyteEntity | None:
        result = await self.session.execute(
            select(AnalyteEntity)
            .options(selectinload(AnalyteEntity.test_type))
            .where((AnalyteEntity.name == name) & (AnalyteEntity.id != analyte_id))
        )
        return result.scalar_one_or_none()

    async def save_analyte(self, entity: AnalyteEntity) -> AnalyteEntity:
        self.session.add(entity)
        await self.session.commit()
        return await self.get_analyte_by_id(str(entity.id))

    async def update_analyte(self, entity: AnalyteEntity) -> AnalyteEntity:
        merged = await self.session.merge(entity)
        await self.session.commit()
        return await self.get_analyte_by_id(str(merged.id))

    async def delete_analyte(self, analyte_id: str) -> None:
        await self.session.execute(
            delete(AnalyteEntity).where(AnalyteEntity.id == analyte_id)
        )
        await self.session.commit()
