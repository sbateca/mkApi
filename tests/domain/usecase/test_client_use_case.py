from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.client_exception import ClientAlreadyExistsError  # type: ignore
from domain.usecase.client_use_case import ClientUseCase  # type: ignore
from tests.builders import ClientBuilder


@pytest.mark.asyncio
async def test_create_client_assigns_id_and_saves_when_client_does_not_exist():
    # Arrange
    client = ClientBuilder().without_id().build()
    saved_client = (
        ClientBuilder().with_id(UUID("f2edbd83-8ea3-4f95-bc4b-28d33e40f81d")).build()
    )
    persistence_port = AsyncMock()
    persistence_port.get_client_by_email_or_nit.return_value = None
    persistence_port.save_client.return_value = saved_client
    use_case = ClientUseCase(persistence_port)

    # Act
    result = await use_case.create_client(client)

    # Assert
    assert client.id is not None
    assert result == saved_client
    persistence_port.get_client_by_email_or_nit.assert_awaited_once_with(
        client.email,
        client.nit,
    )
    persistence_port.save_client.assert_awaited_once_with(client)


@pytest.mark.asyncio
async def test_create_client_raises_when_email_or_nit_already_exists():
    # Arrange
    client = ClientBuilder().without_id().build()
    stored_client = ClientBuilder().build()
    persistence_port = AsyncMock()
    persistence_port.get_client_by_email_or_nit.return_value = stored_client
    use_case = ClientUseCase(persistence_port)

    # Act / Assert
    with pytest.raises(ClientAlreadyExistsError):
        await use_case.create_client(client)

    persistence_port.get_client_by_email_or_nit.assert_awaited_once_with(
        client.email,
        client.nit,
    )
    persistence_port.save_client.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_client_preserves_existing_id():
    # Arrange
    client_id = UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")
    client = ClientBuilder().with_id(client_id).build()
    persistence_port = AsyncMock()
    persistence_port.get_client_by_email_or_nit.return_value = None
    persistence_port.save_client.return_value = client
    use_case = ClientUseCase(persistence_port)

    # Act
    result = await use_case.create_client(client)

    # Assert
    assert result.id == client_id
    persistence_port.save_client.assert_awaited_once_with(client)


@pytest.mark.asyncio
async def test_get_clients_returns_list_of_clients():
    # Arrange
    client1 = (
        ClientBuilder().with_id(UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")).build()
    )
    client2 = (
        ClientBuilder().with_id(UUID("f2edbd83-8ea3-4f95-bc4b-28d33e40f81d")).build()
    )
    persistence_port = AsyncMock()
    persistence_port.get_clients.return_value = [client1, client2]
    use_case = ClientUseCase(persistence_port)

    # Act
    result = await use_case.get_clients()

    # Assert
    assert result == [client1, client2]
    persistence_port.get_clients.assert_awaited_once()
