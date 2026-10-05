from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from jose import jwt

from domain.util.constants import UserRole
from infrastructure.output.security.jwt_adapter import JwtAdapter
from infrastructure.util.constants import TokenError


def test_create_and_decode_token_round_trip():
    adapter = JwtAdapter("test-secret", "HS256", 60)
    user_id = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")

    authenticated_user = adapter.decode_token(
        adapter.create_token(user_id, [UserRole.ADMIN])
    )

    assert authenticated_user.id == user_id
    assert authenticated_user.roles == frozenset({UserRole.ADMIN})


def test_decode_token_uses_expired_token_error_constant():
    adapter = JwtAdapter("test-secret", "HS256", 60)
    token = jwt.encode(
        {"exp": datetime.now(UTC) - timedelta(seconds=1)},
        "test-secret",
        algorithm="HS256",
    )

    with pytest.raises(ValueError, match=f"^{TokenError.EXPIRED.value}$"):
        adapter.decode_token(token)


def test_decode_token_uses_invalid_token_error_constant():
    adapter = JwtAdapter("test-secret", "HS256", 60)

    with pytest.raises(ValueError, match=f"^{TokenError.INVALID.value}$"):
        adapter.decode_token("not-a-token")
