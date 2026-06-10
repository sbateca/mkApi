from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.client_entity import ClientEntity


class ClientPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_clients(self) -> list[ClientEntity]:
        result = await self.session.execute(select(ClientEntity))
        return result.scalars().all()

    async def get_client_by_id(self, client_id: str) -> ClientEntity | None:
        result = await self.session.execute(
            select(ClientEntity).where(ClientEntity.id == client_id)
        )
        return result.scalar_one_or_none()

    async def save_client(self, client_entity: ClientEntity) -> ClientEntity:
        self.session.add(client_entity)
        await self.session.commit()
        await self.session.refresh(client_entity)

        return client_entity

    async def get_client_by_email_or_nit(
        self, email: str, nit: str
    ) -> ClientEntity | None:
        result = await self.session.execute(
            select(ClientEntity).where(
                (ClientEntity.email == email) | (ClientEntity.nit == nit)
            )
        )
        return result.scalar_one_or_none()
