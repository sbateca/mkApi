from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.model.sample_type import SampleType as DomainSampleType
from infrastructure.output.postgresql.adapter.sample_type_persistence_adapter import (
    SampleTypePersistenceAdapter as PersistenceAdapter,
)
from infrastructure.output.postgresql.entity.sample_type_entity import (
    SampleTypeEntity as PersistenceEntity,
)
from infrastructure.output.postgresql.mapper.sample_type_entity_mapper import (
    SampleTypeEntityMapper as PersistenceMapper,
)

SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")


def test_sample_type_entity_mapper_maps_both_directions_and_lists():
    mapper = PersistenceMapper()
    domain = DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water")

    entity = mapper.to_entity(domain)
    assert entity.id == SAMPLE_TYPE_ID
    assert mapper.to_domain(entity) == domain
    assert mapper.to_domain_list([entity]) == [domain]


@pytest.mark.asyncio
async def test_sample_type_adapter_maps_and_delegates_all_operations():
    entity = PersistenceEntity(id=SAMPLE_TYPE_ID, name="Bottled water")
    domain = DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water")
    repository = AsyncMock()
    repository.get_sample_types.return_value = [entity]
    repository.get_sample_type_by_id.return_value = entity
    repository.get_sample_type_by_name.return_value = entity
    repository.get_sample_type_by_name_excluding_id.return_value = entity
    repository.save_sample_type.return_value = entity
    repository.update_sample_type.return_value = entity
    adapter = PersistenceAdapter(repository, PersistenceMapper())

    assert await adapter.get_sample_types() == [domain]
    assert await adapter.get_sample_type_by_id(str(SAMPLE_TYPE_ID)) == domain
    assert await adapter.get_sample_type_by_name(domain.name) == domain
    assert (
        await adapter.get_sample_type_by_name_excluding_id(
            domain.name, str(SAMPLE_TYPE_ID)
        )
        == domain
    )
    assert await adapter.save_sample_type(domain) == domain
    assert await adapter.update_sample_type(domain) == domain
    assert await adapter.delete_sample_type(str(SAMPLE_TYPE_ID)) is None
    repository.delete_sample_type.assert_awaited_once_with(str(SAMPLE_TYPE_ID))


@pytest.mark.asyncio
async def test_sample_type_adapter_returns_none_for_missing_entities():
    repository = AsyncMock()
    repository.get_sample_type_by_id.return_value = None
    repository.get_sample_type_by_name.return_value = None
    repository.get_sample_type_by_name_excluding_id.return_value = None
    adapter = PersistenceAdapter(repository, PersistenceMapper())

    assert await adapter.get_sample_type_by_id(str(SAMPLE_TYPE_ID)) is None
    assert await adapter.get_sample_type_by_name("missing") is None
    assert (
        await adapter.get_sample_type_by_name_excluding_id(
            "missing", str(SAMPLE_TYPE_ID)
        )
        is None
    )
