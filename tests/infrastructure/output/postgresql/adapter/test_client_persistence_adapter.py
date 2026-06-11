from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from infrastructure.output.postgresql.adapter.client_persistence_adapter import (  # type: ignore
    ClientPersistenceAdapter,
)
from infrastructure.output.postgresql.mapper.client_entity_mapper import (  # type: ignore
    ClientEntityMapper,
)
from tests.builders import ClientBuilder, ClientEntityBuilder


@pytest.mark.asyncio
async def test_save_client_maps_domain_to_entity_and_returns_saved_domain_model():
    # Arrange
    client = ClientBuilder().build()
    saved_entity = ClientEntityBuilder().build()
    repository = AsyncMock()
    repository.save_client.return_value = saved_entity
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.save_client(client)

    # Assert
    repository.save_client.assert_awaited_once()
    delegated_entity = repository.save_client.await_args.args[0]
    assert delegated_entity.id == client.id
    assert delegated_entity.email == client.email
    assert result.id == saved_entity.id
    assert result.email == saved_entity.email


@pytest.mark.asyncio
async def test_get_client_by_email_or_nit_returns_domain_model_when_entity_exists():
    # Arrange
    client_entity = ClientEntityBuilder().build()
    repository = AsyncMock()
    repository.get_client_by_email_or_nit.return_value = client_entity
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_client_by_email_or_nit(
        client_entity.email,
        client_entity.nit,
    )

    # Assert
    repository.get_client_by_email_or_nit.assert_awaited_once_with(
        client_entity.email,
        client_entity.nit,
    )
    assert result is not None
    assert result.id == client_entity.id
    assert result.email == client_entity.email


@pytest.mark.asyncio
async def test_get_client_by_email_or_nit_returns_none_when_entity_does_not_exist():
    # Arrange
    repository = AsyncMock()
    repository.get_client_by_email_or_nit.return_value = None
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_client_by_email_or_nit(
        "missing@example.com",
        "missing-nit",
    )

    # Assert
    assert result is None
    repository.get_client_by_email_or_nit.assert_awaited_once_with(
        "missing@example.com",
        "missing-nit",
    )


@pytest.mark.asyncio
async def test_get_client_by_email_or_nit_excluding_client_id_returns_domain_model_when_entity_exists():
    # Arrange
    client_id = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"
    client_entity = ClientEntityBuilder().build()
    repository = AsyncMock()
    repository.get_client_by_email_or_nit_excluding_client_id.return_value = (
        client_entity
    )
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_client_by_email_or_nit_excluding_client_id(
        client_entity.email,
        client_entity.nit,
        client_id,
    )

    # Assert
    repository.get_client_by_email_or_nit_excluding_client_id.assert_awaited_once_with(
        client_entity.email,
        client_entity.nit,
        client_id,
    )
    assert result is not None
    assert result.id == client_entity.id
    assert result.email == client_entity.email


@pytest.mark.asyncio
async def test_get_client_by_email_or_nit_excluding_client_id_returns_none_when_entity_does_not_exist():
    # Arrange
    client_id = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"
    repository = AsyncMock()
    repository.get_client_by_email_or_nit_excluding_client_id.return_value = None
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_client_by_email_or_nit_excluding_client_id(
        "missing@example.com",
        "missing-nit",
        client_id,
    )

    # Assert
    assert result is None
    repository.get_client_by_email_or_nit_excluding_client_id.assert_awaited_once_with(
        "missing@example.com",
        "missing-nit",
        client_id,
    )


@pytest.mark.asyncio
async def test_get_clients_returns_list_of_domain_models():
    # Arrange
    client_entity1 = (
        ClientEntityBuilder().with_id("08dfffe2-c197-4726-b6ab-1e253c8e5f46").build()
    )
    client_entity2 = (
        ClientEntityBuilder().with_id("12345678-1234-5678-1234-567812345678").build()
    )
    repository = AsyncMock()
    repository.get_clients.return_value = [client_entity1, client_entity2]
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_clients()

    # Assert
    repository.get_clients.assert_awaited_once()
    assert len(result) == 2
    assert result[0].id == client_entity1.id
    assert result[0].email == client_entity1.email
    assert result[1].id == client_entity2.id
    assert result[1].email == client_entity2.email


@pytest.mark.asyncio
async def test_get_client_by_id_returns_domain_model_when_entity_exists():
    # Arrange
    client_id = UUID("08dfffe2-c197-4726-b6ab-1e253c8e5f46")
    client_entity = ClientEntityBuilder().with_id(client_id).build()
    repository = AsyncMock()
    repository.get_client_by_id.return_value = client_entity
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_client_by_id(str(client_id))

    # Assert
    repository.get_client_by_id.assert_awaited_once_with(str(client_id))
    assert result is not None
    assert result.id == client_entity.id
    assert result.email == client_entity.email


@pytest.mark.asyncio
async def test_get_client_by_id_returns_none_when_entity_does_not_exist():
    # Arrange
    client_id = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"
    repository = AsyncMock()
    repository.get_client_by_id.return_value = None
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.get_client_by_id(client_id)

    # Assert
    assert result is None
    repository.get_client_by_id.assert_awaited_once_with(client_id)


@pytest.mark.asyncio
async def test_update_client_maps_domain_to_entity_and_returns_updated_domain_model():
    # Arrange
    client = (
        ClientBuilder()
        .with_name("Updated Labs")
        .with_email("updated@example.com")
        .with_phone("3011111111")
        .with_nit("901111111")
        .with_address("New Street 456")
        .build()
    )
    updated_entity = (
        ClientEntityBuilder()
        .with_id(client.id)
        .with_name(client.name)
        .with_email(client.email)
        .with_phone(client.phone)
        .with_nit(client.nit)
        .with_address(client.address)
        .build()
    )
    repository = AsyncMock()
    repository.update_client.return_value = updated_entity
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.update_client(client)

    # Assert
    repository.update_client.assert_awaited_once()
    delegated_entity = repository.update_client.await_args.args[0]
    assert delegated_entity.id == client.id
    assert delegated_entity.name == client.name
    assert delegated_entity.email == client.email
    assert delegated_entity.phone == client.phone
    assert delegated_entity.nit == client.nit
    assert delegated_entity.address == client.address
    assert result.id == updated_entity.id
    assert result.email == updated_entity.email


@pytest.mark.asyncio
async def test_delete_client_delegates_to_repository():
    # Arrange
    client_id = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"
    repository = AsyncMock()
    adapter = ClientPersistenceAdapter(
        client_repository=repository,
        client_entity_mapper=ClientEntityMapper(),
    )

    # Act
    result = await adapter.delete_client(client_id)

    # Assert
    assert result is None
    repository.delete_client.assert_awaited_once_with(client_id)
