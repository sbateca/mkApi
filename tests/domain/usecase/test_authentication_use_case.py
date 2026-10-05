from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from domain.exception.authentication_exception import AuthenticationError
from domain.model.login_data import LoginData
from domain.model.role import Role
from domain.model.user import User
from domain.usecase.authentication_use_case import AuthenticationUseCase
from domain.util.constants import UserRole

USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


def make_user() -> User:
    return User(
        id=USER_ID,
        name="Admin",
        username="admin",
        password="stored-hash",
        email="admin@example.com",
        roles=[Role(name=UserRole.ADMIN), Role(name=UserRole.ANALYST)],
    )


def make_use_case(persistence=None, refresh_tokens=None, generator=None):
    generator = generator or Mock()
    generator.generate.return_value = "new-refresh-token"
    generator.digest.side_effect = lambda token: f"hash:{token}"
    return AuthenticationUseCase(
        persistence or AsyncMock(),
        Mock(),
        Mock(),
        refresh_tokens or AsyncMock(),
        generator,
        2_592_000,
    )


@pytest.mark.asyncio
async def test_login_verifies_password_and_persists_refresh_token():
    persistence = AsyncMock()
    persistence.find_by_username.return_value = make_user()
    refresh_tokens = AsyncMock()
    use_case = make_use_case(persistence, refresh_tokens)
    use_case.password_hasher_port.verify.return_value = True
    use_case.token_port.create_token.return_value = "access-token"

    result = await use_case.login(LoginData(username="admin", password="secret"))

    assert result.access_token == "access-token"
    assert result.refresh_token == "new-refresh-token"
    use_case.password_hasher_port.verify.assert_called_once_with(
        "secret", "stored-hash"
    )
    refresh_tokens.save.assert_awaited_once()
    assert refresh_tokens.save.await_args.args[:2] == (
        "hash:new-refresh-token",
        USER_ID,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_exists,password_matches", [(False, False), (True, False)]
)
async def test_login_rejects_unknown_user_or_invalid_password(
    user_exists, password_matches
):
    persistence = AsyncMock()
    persistence.find_by_username.return_value = make_user() if user_exists else None
    use_case = make_use_case(persistence)
    use_case.password_hasher_port.verify.return_value = password_matches

    with pytest.raises(AuthenticationError):
        await use_case.login(LoginData(username="admin", password="wrong"))

    use_case.token_port.create_token.assert_not_called()


@pytest.mark.asyncio
async def test_refresh_rotates_token_and_returns_new_pair():
    persistence = AsyncMock()
    persistence.find_by_id.return_value = make_user()
    refresh_tokens = AsyncMock()
    refresh_tokens.rotate.return_value = USER_ID
    use_case = make_use_case(persistence, refresh_tokens)
    use_case.token_port.create_token.return_value = "new-access-token"

    result = await use_case.refresh("old-refresh-token")

    assert result.access_token == "new-access-token"
    assert result.refresh_token == "new-refresh-token"
    refresh_tokens.rotate.assert_awaited_once()
    assert refresh_tokens.rotate.await_args.args[:2] == (
        "hash:old-refresh-token",
        "hash:new-refresh-token",
    )


@pytest.mark.asyncio
async def test_refresh_rejects_expired_revoked_or_reused_token():
    refresh_tokens = AsyncMock()
    refresh_tokens.rotate.return_value = None
    use_case = make_use_case(refresh_tokens=refresh_tokens)

    with pytest.raises(AuthenticationError):
        await use_case.refresh("invalid-refresh-token")


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token():
    refresh_tokens = AsyncMock()
    use_case = make_use_case(refresh_tokens=refresh_tokens)

    await use_case.logout("refresh-token")

    refresh_tokens.revoke.assert_awaited_once_with("hash:refresh-token")
