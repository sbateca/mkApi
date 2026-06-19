from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.model.test_type import TestType as DomainTestType
from infrastructure.output.postgresql.adapter.test_type_persistence_adapter import (
    TestTypePersistenceAdapter as TypePersistenceAdapter,
)
from infrastructure.output.postgresql.entity.test_type_entity import (
    TestTypeEntity as TypeEntity,
)
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper as TypeEntityMapper,
)

TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


def test_test_type_entity_mapper_maps_both_directions_and_lists():
    mapper = TypeEntityMapper()
    domain = DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")

    entity = mapper.to_entity(domain)
    mapped_domain = mapper.to_domain(entity)
    mapped_list = mapper.to_domain_list([entity])

    assert entity.id == domain.id
    assert entity.name == domain.name
    assert mapped_domain == domain
    assert mapped_list == [domain]


@pytest.mark.asyncio
async def test_test_type_adapter_maps_and_delegates_all_operations():
    entity = TypeEntity(id=TEST_TYPE_ID, name="Physical-Chemical")
    repository = AsyncMock()
    repository.get_test_types.return_value = [entity]
    repository.get_test_type_by_id.return_value = entity
    repository.get_test_type_by_name.return_value = entity
    repository.get_test_type_by_name_excluding_id.return_value = entity
    repository.save_test_type.return_value = entity
    repository.update_test_type.return_value = entity
    adapter = TypePersistenceAdapter(repository, TypeEntityMapper())
    domain = DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")

    assert await adapter.get_test_types() == [domain]
    assert await adapter.get_test_type_by_id(str(TEST_TYPE_ID)) == domain
    assert await adapter.get_test_type_by_name(domain.name) == domain
    assert (
        await adapter.get_test_type_by_name_excluding_id(domain.name, str(TEST_TYPE_ID))
        == domain
    )
    assert await adapter.save_test_type(domain) == domain
    assert await adapter.update_test_type(domain) == domain
    assert await adapter.delete_test_type(str(TEST_TYPE_ID)) is None

    repository.get_test_types.assert_awaited_once()
    repository.get_test_type_by_id.assert_awaited_once_with(str(TEST_TYPE_ID))
    repository.get_test_type_by_name.assert_awaited_once_with(domain.name)
    repository.get_test_type_by_name_excluding_id.assert_awaited_once_with(
        domain.name, str(TEST_TYPE_ID)
    )
    repository.save_test_type.assert_awaited_once()
    repository.update_test_type.assert_awaited_once()
    repository.delete_test_type.assert_awaited_once_with(str(TEST_TYPE_ID))


@pytest.mark.asyncio
async def test_test_type_adapter_returns_none_for_missing_entities():
    repository = AsyncMock()
    repository.get_test_type_by_id.return_value = None
    repository.get_test_type_by_name.return_value = None
    repository.get_test_type_by_name_excluding_id.return_value = None
    adapter = TypePersistenceAdapter(repository, TypeEntityMapper())

    assert await adapter.get_test_type_by_id(str(TEST_TYPE_ID)) is None
    assert await adapter.get_test_type_by_name("Missing") is None
    assert (
        await adapter.get_test_type_by_name_excluding_id("Missing", str(TEST_TYPE_ID))
        is None
    )
