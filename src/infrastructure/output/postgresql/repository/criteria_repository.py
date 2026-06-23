from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.criteria_entity import CriteriaEntity


class CriteriaPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_criteria(self) -> list[CriteriaEntity]:
        result = await self.session.execute(
            select(CriteriaEntity).order_by(CriteriaEntity.name)
        )
        return result.scalars().all()

    async def get_criteria_by_id(self, criteria_id: str) -> CriteriaEntity | None:
        result = await self.session.execute(
            select(CriteriaEntity).where(CriteriaEntity.id == criteria_id)
        )
        return result.scalar_one_or_none()

    async def get_criteria_by_name(self, name: str) -> CriteriaEntity | None:
        result = await self.session.execute(
            select(CriteriaEntity).where(CriteriaEntity.name == name)
        )
        return result.scalar_one_or_none()

    async def get_criteria_by_name_excluding_id(
        self, name: str, criteria_id: str
    ) -> CriteriaEntity | None:
        result = await self.session.execute(
            select(CriteriaEntity).where(
                (CriteriaEntity.name == name) & (CriteriaEntity.id != criteria_id)
            )
        )
        return result.scalar_one_or_none()

    async def save_criteria(self, entity: CriteriaEntity) -> CriteriaEntity:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update_criteria(self, entity: CriteriaEntity) -> CriteriaEntity:
        merged = await self.session.merge(entity)
        await self.session.commit()
        await self.session.refresh(merged)
        return merged

    async def delete_criteria(self, criteria_id: str) -> None:
        await self.session.execute(
            delete(CriteriaEntity).where(CriteriaEntity.id == criteria_id)
        )
        await self.session.commit()
