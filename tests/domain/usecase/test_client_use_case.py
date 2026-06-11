from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.client_exception import (  # type: ignore
    ClientAlreadyExistsError,
    ClientNotFoundError,
)
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


@pytest.mark.asyncio
async def test_get_client_by_id_returns_client_when_found():
    # Arrange
    client_id = UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")
    client = ClientBuilder().with_id(client_id).build()
    persistence_port = AsyncMock()
    persistence_port.get_client_by_id.return_value = client
    use_case = ClientUseCase(persistence_port)

    # Act
    result = await use_case.get_client_by_id(str(client_id))

    # Assert
    assert result == client
    persistence_port.get_client_by_id.assert_awaited_once_with(str(client_id))


@pytest.mark.asyncio
async def test_get_client_by_id_raises_when_client_does_not_exist():
    # Arrange
    client_id = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"
    persistence_port = AsyncMock()
    persistence_port.get_client_by_id.return_value = None
    use_case = ClientUseCase(persistence_port)

    # Act / Assert
    with pytest.raises(ClientNotFoundError):
        await use_case.get_client_by_id(client_id)

    persistence_port.get_client_by_id.assert_awaited_once_with(client_id)


@pytest.mark.asyncio
async def test_update_client_updates_existing_client_and_persists_changes():
    # Arrange
    client_id = UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")
    current_client = (
        ClientBuilder()
        .with_id(client_id)
        .with_email("current@example.com")
        .with_phone("3000000000")
        .with_nit("900000000")
        .with_address("Old Street 123")
        .build()
    )
    updated_client = (
        ClientBuilder()
        .without_id()
        .with_name("Updated Labs")
        .with_email("updated@example.com")
        .with_phone("3011111111")
        .with_nit("901111111")
        .with_address("New Street 456")
        .build()
    )
    persistence_port = AsyncMock()
    persistence_port.get_client_by_id.return_value = current_client
    persistence_port.get_client_by_email_or_nit_excluding_client_id.return_value = None
    persistence_port.update_client.return_value = current_client
    use_case = ClientUseCase(persistence_port)

    # Act
    result = await use_case.update_client(str(client_id), updated_client)

    # Assert
    assert result == current_client
    assert current_client.id == client_id
    assert current_client.name == updated_client.name
    assert current_client.email == updated_client.email
    assert current_client.phone == updated_client.phone
    assert current_client.nit == updated_client.nit
    assert current_client.address == updated_client.address
    persistence_port.get_client_by_id.assert_awaited_once_with(str(client_id))
    persistence_port.get_client_by_email_or_nit_excluding_client_id.assert_awaited_once_with(
        updated_client.email,
        updated_client.nit,
        client_id,
    )
    persistence_port.update_client.assert_awaited_once_with(current_client)


@pytest.mark.asyncio
async def test_update_client_allows_email_or_nit_that_belongs_to_same_client():
    # Arrange
    client_id = UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")
    current_client = ClientBuilder().with_id(client_id).build()
    updated_client = (
        ClientBuilder()
        .without_id()
        .with_name("Updated Labs")
        .with_address("New Street 456")
        .build()
    )
    persistence_port = AsyncMock()
    persistence_port.get_client_by_id.return_value = current_client
    persistence_port.get_client_by_email_or_nit_excluding_client_id.return_value = None
    persistence_port.update_client.return_value = current_client
    use_case = ClientUseCase(persistence_port)

    # Act
    result = await use_case.update_client(str(client_id), updated_client)

    # Assert
    assert result == current_client
    persistence_port.get_client_by_email_or_nit_excluding_client_id.assert_awaited_once_with(
        updated_client.email,
        updated_client.nit,
        client_id,
    )
    persistence_port.update_client.assert_awaited_once_with(current_client)


@pytest.mark.asyncio
async def test_update_client_raises_when_client_does_not_exist():
    # Arrange
    client_id = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"
    updated_client = ClientBuilder().without_id().build()
    persistence_port = AsyncMock()
    persistence_port.get_client_by_id.return_value = None
    use_case = ClientUseCase(persistence_port)

    # Act / Assert
    with pytest.raises(ClientNotFoundError):
        await use_case.update_client(client_id, updated_client)

    persistence_port.get_client_by_id.assert_awaited_once_with(client_id)
    persistence_port.get_client_by_email_or_nit_excluding_client_id.assert_not_awaited()
    persistence_port.update_client.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_client_raises_when_email_or_nit_belongs_to_another_client():
    # Arrange
    client_id = UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")
    other_client_id = UUID("12345678-1234-5678-1234-567812345678")
    current_client = ClientBuilder().with_id(client_id).build()
    stored_client = ClientBuilder().with_id(other_client_id).build()
    updated_client = (
        ClientBuilder()
        .without_id()
        .with_email(stored_client.email)
        .with_nit(stored_client.nit)
        .build()
    )
    persistence_port = AsyncMock()
    persistence_port.get_client_by_id.return_value = current_client
    persistence_port.get_client_by_email_or_nit_excluding_client_id.return_value = (
        stored_client
    )
    use_case = ClientUseCase(persistence_port)

    # Act / Assert
    with pytest.raises(ClientAlreadyExistsError):
        await use_case.update_client(str(client_id), updated_client)

    persistence_port.get_client_by_email_or_nit_excluding_client_id.assert_awaited_once_with(
        updated_client.email,
        updated_client.nit,
        client_id,
    )
    persistence_port.update_client.assert_not_awaited()
