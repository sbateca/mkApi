from unittest.mock import AsyncMock

import pytest

from application.dto.request.get_client_by_id_request_dto import (  # type: ignore
    GetClientByIdRequestDto,
)
from application.dto.request.update_client_request_dto import (  # type: ignore
    UpdateClientRequestDto,
)
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


@pytest.mark.asyncio
async def test_get_clients_delegates_to_service_and_maps_response():
    # Arrange
    clients = [ClientBuilder().build(), ClientBuilder().build()]
    client_service_port = AsyncMock()
    client_service_port.get_clients.return_value = clients
    handler = ClientHandler(
        client_mapper=ClientMapper(),
        client_service_port=client_service_port,
    )

    # Act
    result = await handler.get_clients()

    # Assert
    client_service_port.get_clients.assert_awaited_once()
    assert len(result) == len(clients)
    for i in range(len(clients)):
        assert result[i].id == clients[i].id
        assert result[i].email == clients[i].email


@pytest.mark.asyncio
async def test_get_client_by_id_delegates_to_service_and_maps_response():
    # Arrange
    client = ClientBuilder().build()
    request = GetClientByIdRequestDto(client_id=str(client.id))
    client_service_port = AsyncMock()
    client_service_port.get_client_by_id.return_value = client
    handler = ClientHandler(
        client_mapper=ClientMapper(),
        client_service_port=client_service_port,
    )

    # Act
    result = await handler.get_client_by_id(request)

    # Assert
    client_service_port.get_client_by_id.assert_awaited_once_with(str(client.id))
    assert result.id == client.id
    assert result.email == client.email


@pytest.mark.asyncio
async def test_update_client_maps_request_delegates_to_service_and_maps_response():
    # Arrange
    client = ClientBuilder().build()
    request_client = (
        CreateClientRequestDtoBuilder()
        .with_name("Updated Labs")
        .with_email("updated@example.com")
        .with_phone("3011111111")
        .with_nit("901111111")
        .with_address("New Street 456")
        .build()
    )
    request = UpdateClientRequestDto(
        client_id=str(client.id),
        client=request_client,
    )
    client_service_port = AsyncMock()
    client_service_port.update_client.return_value = client
    handler = ClientHandler(
        client_mapper=ClientMapper(),
        client_service_port=client_service_port,
    )

    # Act
    result = await handler.update_client(request)

    # Assert
    client_service_port.update_client.assert_awaited_once()
    delegated_client_id, delegated_client = (
        client_service_port.update_client.await_args.args
    )
    assert delegated_client_id == str(client.id)
    assert delegated_client.id is None
    assert delegated_client.name == request_client.name
    assert delegated_client.email == request_client.email
    assert delegated_client.phone == request_client.phone
    assert delegated_client.nit == request_client.nit
    assert delegated_client.address == request_client.address
    assert result.id == client.id
    assert result.email == client.email
