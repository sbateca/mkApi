from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response.login_response_dto import LoginResponseDto
from domain.exception.authentication_exception import AuthenticationError
from infrastructure.configuration.dependencies import get_authentication_handler
from main import app


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
