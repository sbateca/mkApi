from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.exception.analyte_exception import AnalyteAlreadyExistsError
from infrastructure.output.postgresql.entity.analyte_entity import (
    ANALYTE_NAME_TEST_TYPE_INDEX,
    AnalyteEntity,
)


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

    async def get_analyte_by_name(
        self, name: str, test_type_id: UUID
    ) -> AnalyteEntity | None:
        result = await self.session.execute(
            select(AnalyteEntity)
            .options(selectinload(AnalyteEntity.test_type))
            .where(
                AnalyteEntity.name == name, AnalyteEntity.test_type_id == test_type_id
            )
        )
        return result.scalar_one_or_none()

    async def get_analyte_by_name_excluding_id(
        self, name: str, test_type_id: UUID, analyte_id: str
    ) -> AnalyteEntity | None:
        result = await self.session.execute(
            select(AnalyteEntity)
            .options(selectinload(AnalyteEntity.test_type))
            .where(
                AnalyteEntity.name == name,
                AnalyteEntity.test_type_id == test_type_id,
                AnalyteEntity.id != analyte_id,
            )
        )
        return result.scalar_one_or_none()

    async def save_analyte(self, entity: AnalyteEntity) -> AnalyteEntity:
        self.session.add(entity)
        await self._commit()
        return await self.get_analyte_by_id(str(entity.id))

    async def update_analyte(self, entity: AnalyteEntity) -> AnalyteEntity:
        await self.session.merge(entity)
        await self._commit()
        return await self.get_analyte_by_id(str(entity.id))

    async def _commit(self) -> None:
        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            constraint = getattr(error.orig.__cause__, "constraint_name", None)
            if constraint == ANALYTE_NAME_TEST_TYPE_INDEX:
                raise AnalyteAlreadyExistsError() from error
            raise

    async def delete_analyte(self, analyte_id: str) -> None:
        await self.session.execute(
            delete(AnalyteEntity).where(AnalyteEntity.id == analyte_id)
        )
        await self.session.commit()
