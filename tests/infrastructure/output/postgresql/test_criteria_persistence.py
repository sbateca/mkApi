from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.model.criteria import Criteria as DomainCriteria
from infrastructure.output.postgresql.adapter.criteria_persistence_adapter import (
    CriteriaPersistenceAdapter as PersistenceAdapter,
)
from infrastructure.output.postgresql.entity.criteria_entity import (
    CriteriaEntity as PersistenceEntity,
)
from infrastructure.output.postgresql.mapper.criteria_entity_mapper import (
    CriteriaEntityMapper as PersistenceMapper,
)

CRITERIA_ID = UUID("b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3")


def test_criteria_entity_mapper_maps_both_directions_and_lists():
    mapper = PersistenceMapper()
    domain = DomainCriteria(id=CRITERIA_ID, name="0 UFC/100 ml")

    entity = mapper.to_entity(domain)
    assert entity.id == CRITERIA_ID
    assert mapper.to_domain(entity) == domain
    assert mapper.to_domain_list([entity]) == [domain]


@pytest.mark.asyncio
async def test_criteria_adapter_maps_and_delegates_all_operations():
    entity = PersistenceEntity(id=CRITERIA_ID, name="0 UFC/100 ml")
    domain = DomainCriteria(id=CRITERIA_ID, name="0 UFC/100 ml")
    repository = AsyncMock()
    repository.get_criteria.return_value = [entity]
    repository.get_criteria_by_id.return_value = entity
    repository.get_criteria_by_name.return_value = entity
    repository.get_criteria_by_name_excluding_id.return_value = entity
    repository.save_criteria.return_value = entity
    repository.update_criteria.return_value = entity
    adapter = PersistenceAdapter(repository, PersistenceMapper())

    assert await adapter.get_criteria() == [domain]
    assert await adapter.get_criteria_by_id(str(CRITERIA_ID)) == domain
    assert await adapter.get_criteria_by_name(domain.name) == domain
    assert (
        await adapter.get_criteria_by_name_excluding_id(domain.name, str(CRITERIA_ID))
        == domain
    )
    assert await adapter.save_criteria(domain) == domain
    assert await adapter.update_criteria(domain) == domain
    assert await adapter.delete_criteria(str(CRITERIA_ID)) is None
    repository.delete_criteria.assert_awaited_once_with(str(CRITERIA_ID))


@pytest.mark.asyncio
async def test_criteria_adapter_returns_none_for_missing_entities():
    repository = AsyncMock()
    repository.get_criteria_by_id.return_value = None
    repository.get_criteria_by_name.return_value = None
    repository.get_criteria_by_name_excluding_id.return_value = None
    adapter = PersistenceAdapter(repository, PersistenceMapper())

    assert await adapter.get_criteria_by_id(str(CRITERIA_ID)) is None
    assert await adapter.get_criteria_by_name("missing") is None
    assert (
        await adapter.get_criteria_by_name_excluding_id("missing", str(CRITERIA_ID))
        is None
    )
