from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from infrastructure.output.postgresql.entity.refresh_token_entity import (
    RefreshTokenEntity,
)
from infrastructure.output.postgresql.repository.refresh_token_repository import (
    RefreshTokenPostgreSQLRepository,
)

TOKEN_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")
FAMILY_ID = UUID("b43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")
USER_ID = UUID("c43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


def make_session():
    session = Mock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    return session


def make_token(*, revoked=False):
    return RefreshTokenEntity(
        id=TOKEN_ID,
        family_id=FAMILY_ID,
        token_hash="old-hash",
        user_id=USER_ID,
        expires_at=datetime.now(UTC) + timedelta(days=1),
        revoked_at=datetime.now(UTC) if revoked else None,
    )


@pytest.mark.asyncio
async def test_rotate_revokes_current_token_and_preserves_family():
    session = make_session()
    result = Mock()
    current = make_token()
    result.scalar_one_or_none.return_value = current
    session.execute.return_value = result
    repository = RefreshTokenPostgreSQLRepository(session)

    user_id = await repository.rotate(
        "old-hash",
        "new-hash",
        datetime.now(UTC) + timedelta(days=30),
    )

    replacement = session.add.call_args.args[0]
    assert user_id == USER_ID
    assert current.revoked_at is not None
    assert current.replaced_by_token_id == replacement.id
    assert replacement.family_id == FAMILY_ID
    assert replacement.token_hash == "new-hash"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_reusing_rotated_token_revokes_entire_family():
    session = make_session()
    result = Mock()
    result.scalar_one_or_none.return_value = make_token(revoked=True)
    session.execute.side_effect = [result, Mock()]
    repository = RefreshTokenPostgreSQLRepository(session)

    user_id = await repository.rotate(
        "old-hash",
        "attacker-hash",
        datetime.now(UTC) + timedelta(days=30),
    )

    assert user_id is None
    assert session.execute.await_count == 2
    session.add.assert_not_called()
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_logout_revokes_entire_token_family():
    session = make_session()
    result = Mock()
    result.scalar_one_or_none.return_value = make_token()
    session.execute.side_effect = [result, Mock()]
    repository = RefreshTokenPostgreSQLRepository(session)

    await repository.revoke("old-hash")

    assert session.execute.await_count == 2
    session.commit.assert_awaited_once()
