from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.refresh_token_entity import (
    RefreshTokenEntity,
)


class RefreshTokenPostgreSQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, token_hash: str, user_id: UUID, expires_at: datetime) -> None:
        self.session.add(
            RefreshTokenEntity(
                family_id=uuid4(),
                token_hash=token_hash,
                user_id=user_id,
                expires_at=expires_at,
            )
        )
        await self.session.commit()

    async def rotate(
        self,
        current_token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
    ) -> UUID | None:
        result = await self.session.execute(
            select(RefreshTokenEntity)
            .where(RefreshTokenEntity.token_hash == current_token_hash)
            .with_for_update()
        )
        current = result.scalar_one_or_none()
        if current is None:
            return None

        now = datetime.now(UTC)
        if current.revoked_at is not None:
            await self._revoke_family(current.family_id, now)
            await self.session.commit()
            return None

        if current.expires_at <= now:
            current.revoked_at = now
            await self.session.commit()
            return None

        new_token_id = uuid4()
        current.revoked_at = now
        current.replaced_by_token_id = new_token_id
        self.session.add(
            RefreshTokenEntity(
                id=new_token_id,
                family_id=current.family_id,
                token_hash=new_token_hash,
                user_id=current.user_id,
                expires_at=new_expires_at,
            )
        )
        await self.session.commit()
        return current.user_id

    async def revoke(self, token_hash: str) -> None:
        result = await self.session.execute(
            select(RefreshTokenEntity)
            .where(RefreshTokenEntity.token_hash == token_hash)
            .with_for_update()
        )
        token = result.scalar_one_or_none()
        if token is not None:
            await self._revoke_family(token.family_id, datetime.now(UTC))
            await self.session.commit()

    async def _revoke_family(self, family_id: UUID, revoked_at: datetime) -> None:
        await self.session.execute(
            update(RefreshTokenEntity)
            .where(
                RefreshTokenEntity.family_id == family_id,
                RefreshTokenEntity.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )
