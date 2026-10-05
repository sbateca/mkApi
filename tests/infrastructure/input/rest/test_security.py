from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient

from domain.model.authenticated_user import AuthenticatedUser
from domain.util.constants import UserRole
from infrastructure.configuration.dependencies import get_jwt_adapter
from infrastructure.input.rest.security.authentication import (
    get_authenticated_user,
    require_roles,
)
from main import app


def security_app(dependency) -> FastAPI:
    test_app = FastAPI()

    @test_app.get("/private", dependencies=[Depends(dependency)])
    async def private_endpoint():
        return {"ok": True}

    return test_app


@pytest.mark.asyncio
async def test_protected_endpoint_rejects_missing_token():
    test_app = security_app(get_authenticated_user)

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        response = await client.get("/private")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_application_protects_non_authentication_routers():
    app.dependency_overrides.pop(get_authenticated_user, None)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/clients")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_protected_endpoint_accepts_valid_token():
    token_port = Mock()
    token_port.decode_token.return_value = AuthenticatedUser(
        id=UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e"),
        roles=frozenset({UserRole.ANALYST}),
    )
    test_app = security_app(get_authenticated_user)
    test_app.dependency_overrides[get_jwt_adapter] = lambda: token_port

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/private", headers={"Authorization": "Bearer signed-token"}
        )

    assert response.status_code == 200
    token_port.decode_token.assert_called_once_with("signed-token")


@pytest.mark.asyncio
async def test_role_protected_endpoint_rejects_user_without_role():
    test_app = security_app(require_roles(UserRole.ADMIN))
    test_app.dependency_overrides[get_authenticated_user] = lambda: AuthenticatedUser(
        id=UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e"),
        roles=frozenset({UserRole.ANALYST}),
    )

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        response = await client.get("/private")

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"
