from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from domain.exception.client_exception import ClientNotFoundError  # type: ignore
from infrastructure.configuration.dependencies import get_client_handler  # type: ignore
from infrastructure.util.constants import ClientErrorType  # type: ignore
from main import app  # type: ignore
from tests.builders import ClientResponseDtoBuilder, CreateClientRequestDtoBuilder


@pytest.mark.asyncio
async def test_create_client_returns_created_response_from_handler():
    # Arrange
    response = ClientResponseDtoBuilder().build()
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


@pytest.mark.asyncio
async def test_create_client_returns_validation_error_for_missing_fields():
    # Arrange
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        request_body = CreateClientRequestDtoBuilder().build_dict()
        del request_body["name"]

        # Act
        result = await client.post("/clients", json=request_body)

    # Assert
    assert result.status_code == 422
    assert result.json()["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_get_clients_returns_ok_response_from_handler():
    # Arrange
    response = ClientResponseDtoBuilder().build()
    handler = AsyncMock()
    handler.get_clients.return_value = [response]
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            # Act
            result = await client.get("/clients")

        # Assert
        assert result.status_code == 200
        assert result.json() == [
            {
                "id": str(response.id),
                "name": response.name,
                "email": response.email,
                "phone": response.phone,
                "nit": response.nit,
                "address": response.address,
            }
        ]
        handler.get_clients.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_client_by_id_returns_ok_response_from_handler():
    # Arrange
    response = ClientResponseDtoBuilder().build()
    handler = AsyncMock()
    handler.get_client_by_id.return_value = response
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            # Act
            result = await client.get(f"/clients/{response.id}")

        # Assert
        assert result.status_code == 200
        assert result.json() == {
            "id": str(response.id),
            "name": response.name,
            "email": response.email,
            "phone": response.phone,
            "nit": response.nit,
            "address": response.address,
        }
        handler.get_client_by_id.assert_awaited_once()
        delegated_request = handler.get_client_by_id.await_args.args[0]
        assert delegated_request.client_id == str(response.id)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_client_by_id_returns_not_found_when_handler_raises():
    # Arrange
    client_id = "f2edbd83-8ea3-4f95-bc4b-28d33e40f81d"
    handler = AsyncMock()
    handler.get_client_by_id.side_effect = ClientNotFoundError()
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            # Act
            result = await client.get(f"/clients/{client_id}")

        # Assert
        assert result.status_code == 404
        assert result.json()["type"] == ClientErrorType.CLIENT_NOT_FOUND.value
        assert result.json()["message"] == "The client was not found."
        handler.get_client_by_id.assert_awaited_once()
        delegated_request = handler.get_client_by_id.await_args.args[0]
        assert delegated_request.client_id == client_id
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_client_by_id_returns_bad_request_for_invalid_client_id():
    # Arrange
    handler = AsyncMock()
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            # Act
            result = await client.get("/clients/not-a-uuid")

        # Assert
        assert result.status_code == 422
        assert result.json() == {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "errors": [
                {
                    "field": "client_id",
                    "message": "Value error, Client ID must be a valid UUID",
                }
            ],
        }
        handler.get_client_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_update_client_returns_ok_response_from_handler():
    # Arrange
    response = ClientResponseDtoBuilder().build()
    handler = AsyncMock()
    handler.update_client.return_value = response
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            request_body = (
                CreateClientRequestDtoBuilder()
                .with_name("Updated Labs")
                .with_email("updated@example.com")
                .with_phone("3011111111")
                .with_nit("901111111")
                .with_address("New Street 456")
                .build_dict()
            )

            # Act
            result = await client.put(f"/clients/{response.id}", json=request_body)

        # Assert
        assert result.status_code == 200
        assert result.json() == {
            "id": str(response.id),
            "name": response.name,
            "email": response.email,
            "phone": response.phone,
            "nit": response.nit,
            "address": response.address,
        }
        handler.update_client.assert_awaited_once()
        delegated_request = handler.update_client.await_args.args[0]
        assert delegated_request.client_id == str(response.id)
        assert delegated_request.client.name == request_body["name"]
        assert delegated_request.client.email == request_body["email"]
        assert delegated_request.client.phone == request_body["phone"]
        assert delegated_request.client.nit == request_body["nit"]
        assert delegated_request.client.address == request_body["address"]
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_update_client_returns_validation_error_for_invalid_client_id():
    # Arrange
    handler = AsyncMock()
    app.dependency_overrides[get_client_handler] = lambda: handler

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            request_body = CreateClientRequestDtoBuilder().build_dict()

            # Act
            result = await client.put("/clients/not-a-uuid", json=request_body)

        # Assert
        assert result.status_code == 422
        assert result.json() == {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "errors": [
                {
                    "field": "client_id",
                    "message": "Value error, Client ID must be a valid UUID",
                }
            ],
        }
        handler.update_client.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()
