from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.exception.sample_exception import (
    SampleClientChangeWithApprovedReportError,
    SampleNotFoundError,
)
from domain.util.constants import ReportStatus
from infrastructure.output.postgresql.entity.report_entity import ReportEntity
from infrastructure.output.postgresql.entity.sample_entity import SampleEntity


class SamplePostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_samples(self) -> list[SampleEntity]:
        result = await self.session.execute(
            select(SampleEntity)
            .options(
                selectinload(SampleEntity.sample_type),
                selectinload(SampleEntity.client),
            )
            .order_by(SampleEntity.sample_code)
        )
        return result.scalars().all()

    async def get_sample_by_id(self, sample_id: str) -> SampleEntity | None:
        result = await self.session.execute(
            select(SampleEntity)
            .options(
                selectinload(SampleEntity.sample_type),
                selectinload(SampleEntity.client),
            )
            .where(SampleEntity.id == sample_id)
        )
        return result.scalar_one_or_none()

    async def get_sample_by_sample_code(self, sample_code: str) -> SampleEntity | None:
        result = await self.session.execute(
            select(SampleEntity)
            .options(
                selectinload(SampleEntity.sample_type),
                selectinload(SampleEntity.client),
            )
            .where(SampleEntity.sample_code == sample_code)
        )
        return result.scalar_one_or_none()

    async def get_sample_by_sample_code_excluding_id(
        self, sample_code: str, sample_id: str
    ) -> SampleEntity | None:
        result = await self.session.execute(
            select(SampleEntity)
            .options(
                selectinload(SampleEntity.sample_type),
                selectinload(SampleEntity.client),
            )
            .where(
                (SampleEntity.sample_code == sample_code)
                & (SampleEntity.id != sample_id)
            )
        )
        return result.scalar_one_or_none()

    async def save_sample(self, entity: SampleEntity) -> SampleEntity:
        self.session.add(entity)
        await self.session.commit()
        return await self.get_sample_by_id(str(entity.id))

    async def update_sample(self, entity: SampleEntity) -> SampleEntity:
        try:
            result = await self.session.execute(
                select(SampleEntity.client_id)
                .where(SampleEntity.id == entity.id)
                .with_for_update(key_share=True)
            )
            current_client_id = result.scalar_one_or_none()
            if current_client_id is None:
                raise SampleNotFoundError()
            if current_client_id != entity.client_id:
                approved = select(ReportEntity.id).where(
                    ReportEntity.sample_id == entity.id,
                    func.lower(ReportEntity.status) == ReportStatus.APPROVED.value,
                )
                result = await self.session.execute(select(approved.exists()))
                if result.scalar_one():
                    raise SampleClientChangeWithApprovedReportError()
            await self.session.merge(entity)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return await self.get_sample_by_id(str(entity.id))

    async def delete_sample(self, sample_id: str) -> None:
        await self.session.execute(
            delete(SampleEntity).where(SampleEntity.id == sample_id)
        )
        await self.session.commit()
