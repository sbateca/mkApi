from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.sample_type_entity import (
    SampleTypeEntity,
)


class SampleTypePostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sample_types(self) -> list[SampleTypeEntity]:
        result = await self.session.execute(
            select(SampleTypeEntity).order_by(SampleTypeEntity.name)
        )
        return result.scalars().all()

    async def get_sample_type_by_id(
        self, sample_type_id: str
    ) -> SampleTypeEntity | None:
        result = await self.session.execute(
            select(SampleTypeEntity).where(SampleTypeEntity.id == sample_type_id)
        )
        return result.scalar_one_or_none()

    async def get_sample_type_by_name(self, name: str) -> SampleTypeEntity | None:
        result = await self.session.execute(
            select(SampleTypeEntity).where(SampleTypeEntity.name == name)
        )
        return result.scalar_one_or_none()

    async def get_sample_type_by_name_excluding_id(
        self, name: str, sample_type_id: str
    ) -> SampleTypeEntity | None:
        result = await self.session.execute(
            select(SampleTypeEntity).where(
                (SampleTypeEntity.name == name)
                & (SampleTypeEntity.id != sample_type_id)
            )
        )
        return result.scalar_one_or_none()

    async def save_sample_type(self, entity: SampleTypeEntity) -> SampleTypeEntity:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update_sample_type(self, entity: SampleTypeEntity) -> SampleTypeEntity:
        merged = await self.session.merge(entity)
        await self.session.commit()
        await self.session.refresh(merged)
        return merged

    async def delete_sample_type(self, sample_type_id: str) -> None:
        await self.session.execute(
            delete(SampleTypeEntity).where(SampleTypeEntity.id == sample_type_id)
        )
        await self.session.commit()
