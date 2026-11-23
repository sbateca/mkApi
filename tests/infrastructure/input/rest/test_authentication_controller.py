from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response.login_response_dto import LoginResponseDto
from application.dto.response.user_response_dto import UserResponseDto
from domain.exception.authentication_exception import AuthenticationError
from domain.util.constants import UserRole
from infrastructure.configuration.dependencies import (
    get_authentication_handler,
    get_jwt_adapter,
    get_user_handler,
)
from infrastructure.input.rest.security.authentication import get_authenticated_user
from infrastructure.output.security.jwt_adapter import JwtAdapter
from main import app


@pytest.mark.asyncio
async def test_me_returns_current_user_profile():
    app.dependency_overrides.pop(get_authenticated_user, None)
    user_id = uuid4()
    adapter = JwtAdapter("test-secret-key-with-at-least-32-characters", "HS256", 900)
    handler = AsyncMock()
    handler.get_user.return_value = UserResponseDto(
        id=user_id,
        name="Test User",
        username="test",
        email="test@example.com",
        roles=[],
        client_id=None,
    )
    app.dependency_overrides[get_jwt_adapter] = lambda: adapter
    app.dependency_overrides[get_user_handler] = lambda: handler
    try:
        token = adapter.create_token(user_id, [UserRole.ADMIN])
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(
                "/auth/me", headers={"Authorization": f"Bearer {token}"}
            )
        assert response.status_code == 200
        assert response.json() == {
            "id": str(user_id),
            "name": "Test User",
            "username": "test",
            "email": "test@example.com",
            "roles": [],
            "client_id": None,
        }
        assert handler.get_user.await_args.args[0].user_id == str(user_id)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize("authorization", [None, "Bearer invalid"])
async def test_me_requires_valid_access_token(authorization):
    app.dependency_overrides.pop(get_authenticated_user, None)
    adapter = JwtAdapter("test-secret-key-with-at-least-32-characters", "HS256", 900)
    handler = AsyncMock()
    app.dependency_overrides[get_jwt_adapter] = lambda: adapter
    app.dependency_overrides[get_user_handler] = lambda: handler
    try:
        headers = {"Authorization": authorization} if authorization else {}
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/auth/me", headers=headers)
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"
        handler.get_user.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_delegates_to_handler():
    handler = AsyncMock()
    handler.login.return_value = LoginResponseDto(
        access_token="access-token", refresh_token="refresh-token"
    )
    app.dependency_overrides[get_authentication_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/auth/login",
                json={"username": "admin", "password": "secret"},
            )

        assert response.status_code == 200
        assert response.json() == {
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "token_type": "bearer",
        }
        handler.login.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_returns_unauthorized_for_invalid_credentials():
    handler = AsyncMock()
    handler.login.side_effect = AuthenticationError()
    app.dependency_overrides[get_authentication_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/auth/login",
                json={"username": "admin", "password": "wrong"},
            )

        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"
        assert response.json()["type"] == "AUTHENTICATION_FAILED"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_refresh_rotates_refresh_token():
    handler = AsyncMock()
    handler.refresh.return_value = LoginResponseDto(
        access_token="new-access-token", refresh_token="new-refresh-token"
    )
    app.dependency_overrides[get_authentication_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/auth/refresh", json={"refresh_token": "refresh-token"}
            )

        assert response.status_code == 200
        assert response.json()["access_token"] == "new-access-token"
        handler.refresh.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token():
    handler = AsyncMock()
    app.dependency_overrides[get_authentication_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/auth/logout", json={"refresh_token": "refresh-token"}
            )

        assert response.status_code == 204
        handler.logout.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()
