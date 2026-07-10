from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.model.analysis_method import AnalysisMethod as DomainAnalysisMethod
from domain.model.analyte import Analyte as DomainAnalyte
from domain.model.criteria import Criteria as DomainCriteria
from domain.model.test import Test as DomainTest
from domain.model.test_type import TestType as DomainTestType
from infrastructure.output.postgresql.adapter.test_persistence_adapter import (
    TestPersistenceAdapter as PersistenceAdapter,
)
from infrastructure.output.postgresql.entity.analysis_method_entity import (
    AnalysisMethodEntity,
)
from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity
from infrastructure.output.postgresql.entity.criteria_entity import CriteriaEntity
from infrastructure.output.postgresql.entity.test_entity import (
    TestEntity as PersistenceEntity,
)
from infrastructure.output.postgresql.entity.test_type_entity import (
    TestTypeEntity as TypeEntity,
)
from infrastructure.output.postgresql.mapper.analysis_method_entity_mapper import (
    AnalysisMethodEntityMapper,
)
from infrastructure.output.postgresql.mapper.analyte_entity_mapper import (
    AnalyteEntityMapper,
)
from infrastructure.output.postgresql.mapper.criteria_entity_mapper import (
    CriteriaEntityMapper,
)
from infrastructure.output.postgresql.mapper.test_entity_mapper import (
    TestEntityMapper as PersistenceMapper,
)
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper,
)

TEST_ID = UUID("a3c99dfc-b450-4d56-806a-449cb31d94a1")
TEST_TYPE_ID = UUID("2a4a260f-46ac-4efe-ad52-47db61e6d890")
SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
ANALYTE_ID = UUID("3871d51e-a6ed-479d-b94c-6803e5a7c538")
ANALYSIS_METHOD_ID = UUID("61c7e7ea-795a-4c9c-af23-99ba47556d2f")
CRITERIA_ID = UUID("122c8c5c-d55b-4ed7-ab70-266c6fcfb076")


def mapper() -> PersistenceMapper:
    test_type_mapper = TestTypeEntityMapper()
    return PersistenceMapper(
        test_type_mapper,
        AnalyteEntityMapper(test_type_mapper),
        AnalysisMethodEntityMapper(),
        CriteriaEntityMapper(),
    )


def domain_test() -> DomainTest:
    return DomainTest(
        id=TEST_ID,
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physicochemical"),
        sample_id=str(SAMPLE_ID),
        analyte=DomainAnalyte(
            id=ANALYTE_ID,
            name="Chlorine",
            test_type=DomainTestType(id=TEST_TYPE_ID, name="Physicochemical"),
        ),
        analysis_method=DomainAnalysisMethod(id=ANALYSIS_METHOD_ID, name="SM 4500"),
        criteria=DomainCriteria(id=CRITERIA_ID, name="Resolution 2115"),
        result="15 mg/L",
    )


def build_test_entity() -> PersistenceEntity:
    entity = PersistenceEntity(
        id=TEST_ID,
        test_type_id=TEST_TYPE_ID,
        sample_id=SAMPLE_ID,
        analyte_id=ANALYTE_ID,
        analysis_method_id=ANALYSIS_METHOD_ID,
        criteria_id=CRITERIA_ID,
        result="15 mg/L",
    )
    test_type = TypeEntity(id=TEST_TYPE_ID, name="Physicochemical")
    entity.test_type = test_type
    entity.analyte = AnalyteEntity(
        id=ANALYTE_ID,
        name="Chlorine",
        test_type_id=TEST_TYPE_ID,
    )
    entity.analyte.test_type = test_type
    entity.analysis_method = AnalysisMethodEntity(
        id=ANALYSIS_METHOD_ID,
        name="SM 4500",
    )
    entity.criteria = CriteriaEntity(id=CRITERIA_ID, name="Resolution 2115")
    return entity


def test_test_entity_mapper_maps_both_directions_and_lists():
    domain = domain_test()
    entity = build_test_entity()
    persistence_mapper = mapper()

    mapped_entity = persistence_mapper.to_entity(domain)
    assert mapped_entity.id == TEST_ID
    assert mapped_entity.test_type_id == TEST_TYPE_ID
    assert mapped_entity.sample_id == SAMPLE_ID
    assert mapped_entity.analyte_id == ANALYTE_ID
    assert mapped_entity.analysis_method_id == ANALYSIS_METHOD_ID
    assert mapped_entity.criteria_id == CRITERIA_ID
    assert mapped_entity.result == "15 mg/L"
    assert persistence_mapper.to_domain(entity) == domain
    assert persistence_mapper.to_domain_list([entity]) == [domain]


@pytest.mark.asyncio
async def test_test_adapter_maps_and_delegates_all_operations():
    entity = build_test_entity()
    domain = domain_test()
    repository = AsyncMock()
    repository.get_tests.return_value = [entity]
    repository.get_test_by_id.return_value = entity
    repository.save_test.return_value = entity
    repository.update_test.return_value = entity
    adapter = PersistenceAdapter(repository, mapper())

    assert await adapter.get_tests() == [domain]
    assert await adapter.get_test_by_id(str(TEST_ID)) == domain
    assert await adapter.save_test(domain) == domain
    assert await adapter.update_test(domain) == domain
    assert await adapter.delete_test(str(TEST_ID)) is None

    repository.get_tests.assert_awaited_once()
    repository.get_test_by_id.assert_awaited_once_with(str(TEST_ID))
    repository.save_test.assert_awaited_once()
    repository.update_test.assert_awaited_once()
    repository.delete_test.assert_awaited_once_with(str(TEST_ID))


@pytest.mark.asyncio
async def test_test_adapter_returns_none_for_missing_entities():
    repository = AsyncMock()
    repository.get_test_by_id.return_value = None
    adapter = PersistenceAdapter(repository, mapper())

    assert await adapter.get_test_by_id(str(TEST_ID)) is None
