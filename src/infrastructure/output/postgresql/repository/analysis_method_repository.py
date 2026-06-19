from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.analysis_method_entity import (
    AnalysisMethodEntity,
)


class AnalysisMethodPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_analysis_methods(self) -> list[AnalysisMethodEntity]:
        result = await self.session.execute(
            select(AnalysisMethodEntity).order_by(AnalysisMethodEntity.name)
        )
        return result.scalars().all()

    async def get_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethodEntity | None:
        result = await self.session.execute(
            select(AnalysisMethodEntity).where(
                AnalysisMethodEntity.id == analysis_method_id
            )
        )
        return result.scalar_one_or_none()

    async def get_analysis_method_by_name(
        self, name: str
    ) -> AnalysisMethodEntity | None:
        result = await self.session.execute(
            select(AnalysisMethodEntity).where(AnalysisMethodEntity.name == name)
        )
        return result.scalar_one_or_none()

    async def get_analysis_method_by_name_excluding_id(
        self, name: str, analysis_method_id: str
    ) -> AnalysisMethodEntity | None:
        result = await self.session.execute(
            select(AnalysisMethodEntity).where(
                (AnalysisMethodEntity.name == name)
                & (AnalysisMethodEntity.id != analysis_method_id)
            )
        )
        return result.scalar_one_or_none()

    async def save_analysis_method(
        self, analysis_method_entity: AnalysisMethodEntity
    ) -> AnalysisMethodEntity:
        self.session.add(analysis_method_entity)
        await self.session.commit()
        await self.session.refresh(analysis_method_entity)
        return analysis_method_entity

    async def update_analysis_method(
        self, analysis_method_entity: AnalysisMethodEntity
    ) -> AnalysisMethodEntity:
        merged = await self.session.merge(analysis_method_entity)
        await self.session.commit()
        await self.session.refresh(merged)
        return merged

    async def delete_analysis_method(self, analysis_method_id: str) -> None:
        await self.session.execute(
            delete(AnalysisMethodEntity).where(
                AnalysisMethodEntity.id == analysis_method_id
            )
        )
        await self.session.commit()
