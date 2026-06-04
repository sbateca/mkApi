from unittest.mock import AsyncMock

import pytest

from application.handler.impl.client_handler import ClientHandler  # type: ignore
from application.mapper.client_mapper import ClientMapper  # type: ignore
from tests.builders import ClientBuilder, CreateClientRequestDtoBuilder


@pytest.mark.asyncio
async def test_create_client_maps_request_delegates_to_service_and_maps_response():
    # Arrange
    request = CreateClientRequestDtoBuilder().build()
    created_client = ClientBuilder().build()
    client_service_port = AsyncMock()
    client_service_port.create_client.return_value = created_client
    handler = ClientHandler(
        client_mapper=ClientMapper(),
        client_service_port=client_service_port,
    )

    # Act
    result = await handler.create_client(request)

    # Assert
    client_service_port.create_client.assert_awaited_once()
    delegated_client = client_service_port.create_client.await_args.args[0]
    assert delegated_client.id is None
    assert delegated_client.email == request.email
    assert result.id == created_client.id
    assert result.email == created_client.email
