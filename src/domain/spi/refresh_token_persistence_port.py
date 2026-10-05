from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class RefreshTokenPersistencePort(ABC):
    @abstractmethod
    async def save(self, token_hash: str, user_id: UUID, expires_at: datetime) -> None:
        pass

    @abstractmethod
    async def rotate(
        self,
        current_token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
    ) -> UUID | None:
        pass

    @abstractmethod
    async def revoke(self, token_hash: str) -> None:
        pass
