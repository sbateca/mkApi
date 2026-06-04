from unittest.mock import AsyncMock

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
