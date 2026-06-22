from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.model.analyte import Analyte as DomainAnalyte
from domain.model.test_type import TestType as DomainTestType
from infrastructure.output.postgresql.adapter.analyte_persistence_adapter import (
    AnalytePersistenceAdapter as PersistenceAdapter,
)
from infrastructure.output.postgresql.entity.analyte_entity import (
    AnalyteEntity as PersistenceEntity,
)
from infrastructure.output.postgresql.entity.test_type_entity import (
    TestTypeEntity as TypePersistenceEntity,
)
from infrastructure.output.postgresql.mapper.analyte_entity_mapper import (
    AnalyteEntityMapper as PersistenceMapper,
)
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper as TestTypePersistenceMapper,
)

ANALYTE_ID = UUID("7dc56aee-5530-4df9-896f-c63d8d39f28e")
TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


def entity() -> PersistenceEntity:
    item = PersistenceEntity(id=ANALYTE_ID, name="pH", test_type_id=TEST_TYPE_ID)
    item.test_type = TypePersistenceEntity(id=TEST_TYPE_ID, name="Physical-Chemical")
    return item


def domain() -> DomainAnalyte:
    return DomainAnalyte(
        id=ANALYTE_ID,
        name="pH",
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical"),
    )


def test_analyte_entity_mapper_maps_relationship_both_directions():
    mapper = PersistenceMapper(TestTypePersistenceMapper())

    mapped_entity = mapper.to_entity(domain())
    mapped_domain = mapper.to_domain(entity())

    assert mapped_entity.id == ANALYTE_ID
    assert mapped_entity.test_type_id == TEST_TYPE_ID
    assert mapped_domain == domain()
    assert mapper.to_domain_list([entity()]) == [domain()]


@pytest.mark.asyncio
async def test_analyte_adapter_maps_and_delegates_all_operations():
    persistence_entity = entity()
    repository = AsyncMock()
    repository.save_analyte.return_value = persistence_entity
    repository.get_analytes.return_value = [persistence_entity]
    repository.get_analyte_by_id.return_value = persistence_entity
    repository.get_analyte_by_name.return_value = persistence_entity
    repository.get_analyte_by_name_excluding_id.return_value = persistence_entity
    repository.update_analyte.return_value = persistence_entity
    adapter = PersistenceAdapter(
        repository, PersistenceMapper(TestTypePersistenceMapper())
    )

    assert await adapter.save_analyte(domain()) == domain()
    assert await adapter.get_analytes() == [domain()]
    assert await adapter.get_analyte_by_id(str(ANALYTE_ID)) == domain()
    assert await adapter.get_analyte_by_name("pH") == domain()
    assert (
        await adapter.get_analyte_by_name_excluding_id("pH", str(ANALYTE_ID))
        == domain()
    )
    assert await adapter.update_analyte(domain()) == domain()
    assert await adapter.delete_analyte(str(ANALYTE_ID)) is None
    repository.delete_analyte.assert_awaited_once_with(str(ANALYTE_ID))


@pytest.mark.asyncio
async def test_analyte_adapter_returns_none_for_missing_entities():
    repository = AsyncMock()
    repository.get_analyte_by_id.return_value = None
    repository.get_analyte_by_name.return_value = None
    repository.get_analyte_by_name_excluding_id.return_value = None
    adapter = PersistenceAdapter(
        repository, PersistenceMapper(TestTypePersistenceMapper())
    )

    assert await adapter.get_analyte_by_id(str(ANALYTE_ID)) is None
    assert await adapter.get_analyte_by_name("missing") is None
    assert (
        await adapter.get_analyte_by_name_excluding_id("missing", str(ANALYTE_ID))
        is None
    )
