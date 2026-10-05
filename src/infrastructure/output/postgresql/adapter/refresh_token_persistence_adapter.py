from datetime import datetime
from uuid import UUID

from domain.spi.refresh_token_persistence_port import RefreshTokenPersistencePort
from infrastructure.output.postgresql.repository.refresh_token_repository import (
    RefreshTokenPostgreSQLRepository,
)


class RefreshTokenPersistenceAdapter(RefreshTokenPersistencePort):
    def __init__(self, repository: RefreshTokenPostgreSQLRepository):
        self.repository = repository

    async def save(self, token_hash: str, user_id: UUID, expires_at: datetime) -> None:
        await self.repository.save(token_hash, user_id, expires_at)

    async def rotate(
        self,
        current_token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
    ) -> UUID | None:
        return await self.repository.rotate(
            current_token_hash, new_token_hash, new_expires_at
        )

    async def revoke(self, token_hash: str) -> None:
        await self.repository.revoke(token_hash)
