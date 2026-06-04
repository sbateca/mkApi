from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from infrastructure.configuration.dependencies import get_client_handler  # type: ignore
from main import app  # type: ignore
from tests.builders import CreateClientRequestDtoBuilder, CreateClientResponseDtoBuilder


@pytest.mark.asyncio
async def test_create_client_returns_created_response_from_handler():
    # Arrange
    response = CreateClientResponseDtoBuilder().build()
    handler = AsyncMock()
    handler.create_client.return_value = response
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            request_body = CreateClientRequestDtoBuilder().build_dict()

            # Act
            result = await client.post("/clients", json=request_body)

        # Assert
        assert result.status_code == 201
        assert result.json() == {
            "id": str(response.id),
            "name": response.name,
            "email": response.email,
            "phone": response.phone,
            "nit": response.nit,
            "address": response.address,
        }
        handler.create_client.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_client_returns_validation_error_for_invalid_request():
    # Arrange
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        request_body = CreateClientRequestDtoBuilder().build_dict()
        request_body["email"] = "invalid-email"

        # Act
        result = await client.post("/clients", json=request_body)

    # Assert
    assert result.status_code == 422
    assert result.json()["code"] == "VALIDATION_ERROR"
