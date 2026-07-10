from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from domain.exception.analysis_method_exception import AnalysisMethodNotFoundError
from domain.exception.analyte_exception import AnalyteNotFoundError
from domain.exception.criteria_exception import CriteriaNotFoundError
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_exception import TestNotFoundError as MissingTestError
from domain.exception.test_type_exception import (
    TestTypeConsistencyError,
)
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from domain.model.analysis_method import AnalysisMethod
from domain.model.analyte import Analyte
from domain.model.client import Client
from domain.model.criteria import Criteria
from domain.model.sample import Sample
from domain.model.sample_type import SampleType
from domain.model.test import Test as DomainTest
from domain.model.test_type import TestType as DomainTestType
from domain.spi.logger_port import LoggerPort
from domain.usecase.test_use_case import TestUseCase as DomainTestUseCase

TEST_ID = UUID("a3c99dfc-b450-4d56-806a-449cb31d94a1")
TEST_TYPE_ID = UUID("2a4a260f-46ac-4efe-ad52-47db61e6d890")
SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")
CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")
ANALYTE_ID = UUID("3871d51e-a6ed-479d-b94c-6803e5a7c538")
ANALYSIS_METHOD_ID = UUID("61c7e7ea-795a-4c9c-af23-99ba47556d2f")
CRITERIA_ID = UUID("122c8c5c-d55b-4ed7-ab70-266c6fcfb076")


def build_test(result: str = "15 mg/L") -> DomainTest:
    return DomainTest(
        id=TEST_ID,
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physicochemical"),
        sample_id=str(SAMPLE_ID),
        analyte=Analyte(
            id=ANALYTE_ID,
            name="Chlorine",
            test_type=DomainTestType(id=TEST_TYPE_ID, name="Physicochemical"),
        ),
        analysis_method=AnalysisMethod(id=ANALYSIS_METHOD_ID, name="SM 4500"),
        criteria=Criteria(id=CRITERIA_ID, name="Resolution 2115"),
        result=result,
    )


def sample_item() -> Sample:
    return Sample(
        id=SAMPLE_ID,
        sample_code="1001",
        sample_type=SampleType(id=SAMPLE_TYPE_ID, name="Bottled water"),
        client=Client(
            id=CLIENT_ID,
            name="Maximum Hotel",
            email="hotel@example.com",
            phone="5551234",
            nit="123456",
            address="Main street",
        ),
        get_sample_date=date(2024, 7, 2),
        reception_date=date(2023, 10, 1),
        analysis_date=date(2023, 10, 2),
        sample_location="Hotel's restaurant",
        responsable="John Lenon",
    )


def service_with_ports(logger=None):
    test_port = AsyncMock()
    test_type_port = AsyncMock()
    sample_port = AsyncMock()
    analyte_port = AsyncMock()
    analysis_method_port = AsyncMock()
    criteria_port = AsyncMock()
    service = DomainTestUseCase(
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
        logger,
    )
    return (
        service,
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    )


def setup_valid_relations(
    test_type_port,
    sample_port,
    analyte_port,
    analysis_method_port,
    criteria_port,
):
    test_type_port.get_test_type_by_id.return_value = DomainTestType(
        id=TEST_TYPE_ID,
        name="Physicochemical",
    )
    sample_port.get_sample_by_id.return_value = sample_item()
    analyte_port.get_analyte_by_id.return_value = Analyte(
        id=ANALYTE_ID,
        name="Chlorine",
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physicochemical"),
    )
    analysis_method_port.get_analysis_method_by_id.return_value = AnalysisMethod(
        id=ANALYSIS_METHOD_ID,
        name="SM 4500",
    )
    criteria_port.get_criteria_by_id.return_value = Criteria(
        id=CRITERIA_ID,
        name="Resolution 2115",
    )


def setup_test_type_inconsistency(
    test_type_port,
    sample_port,
    analyte_port,
    analysis_method_port,
    criteria_port,
):
    test_type_inconsistency_id = UUID("3b5c1f2e-4d6a-4e8b-9f1c-2a3b4c5d6e7f")

    test_type_port.get_test_type_by_id.return_value = DomainTestType(
        id=TEST_TYPE_ID,
        name="Physicochemical",
    )
    sample_port.get_sample_by_id.return_value = sample_item()
    analyte_port.get_analyte_by_id.return_value = Analyte(
        id=ANALYTE_ID,
        name="Chlorine",
        test_type=DomainTestType(id=test_type_inconsistency_id, name="Physicochemical"),
    )
    analysis_method_port.get_analysis_method_by_id.return_value = AnalysisMethod(
        id=ANALYSIS_METHOD_ID,
        name="SM 4500",
    )
    criteria_port.get_criteria_by_id.return_value = Criteria(
        id=CRITERIA_ID,
        name="Resolution 2115",
    )


@pytest.mark.asyncio
async def test_create_test_validates_relations_assigns_id_and_saves():
    item = build_test()
    item.id = None
    (
        service,
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    ) = service_with_ports()
    setup_valid_relations(
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    )
    test_port.save_test.return_value = item

    result = await service.create_test(item)

    assert result == item
    assert item.id is not None
    test_type_port.get_test_type_by_id.assert_awaited_once_with(str(TEST_TYPE_ID))
    sample_port.get_sample_by_id.assert_awaited_once_with(str(SAMPLE_ID))
    analyte_port.get_analyte_by_id.assert_awaited_once_with(str(ANALYTE_ID))
    analysis_method_port.get_analysis_method_by_id.assert_awaited_once_with(
        str(ANALYSIS_METHOD_ID)
    )
    criteria_port.get_criteria_by_id.assert_awaited_once_with(str(CRITERIA_ID))
    test_port.save_test.assert_awaited_once_with(item)


@pytest.mark.asyncio
async def test_get_tests_and_get_by_id_return_persisted_items():
    item = build_test()
    service, test_port, *_ = service_with_ports()
    test_port.get_tests.return_value = [item]
    test_port.get_test_by_id.return_value = item

    assert await service.get_tests() == [item]
    assert await service.get_test_by_id(str(TEST_ID)) == item


@pytest.mark.asyncio
async def test_get_test_by_id_rejects_missing_item():
    service, test_port, *_ = service_with_ports()
    test_port.get_test_by_id.return_value = None

    with pytest.raises(MissingTestError):
        await service.get_test_by_id(str(TEST_ID))


@pytest.mark.asyncio
async def test_get_tests_logs_success():
    item = build_test()
    logger = MagicMock(spec=LoggerPort)
    service, test_port, *_ = service_with_ports(logger)
    test_port.get_tests.return_value = [item]

    assert await service.get_tests() == [item]

    logger.info.assert_any_call("Retrieving tests")
    logger.info.assert_any_call("Tests retrieved", count=1)


@pytest.mark.asyncio
async def test_get_test_by_id_logs_not_found():
    logger = MagicMock(spec=LoggerPort)
    service, test_port, *_ = service_with_ports(logger)
    test_port.get_test_by_id.return_value = None

    with pytest.raises(MissingTestError):
        await service.get_test_by_id(str(TEST_ID))

    logger.warning.assert_called_once_with("Test not found", test_id=str(TEST_ID))


@pytest.mark.asyncio
async def test_create_test_logs_safe_metadata():
    item = build_test()
    logger = MagicMock(spec=LoggerPort)
    (
        service,
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    ) = service_with_ports(logger)
    setup_valid_relations(
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    )
    test_port.save_test.return_value = item

    await service.create_test(item)

    logger.info.assert_any_call("Creating test", sample_id=str(SAMPLE_ID))
    logger.info.assert_any_call("Test created", test_id=str(TEST_ID))


@pytest.mark.asyncio
async def test_update_test_updates_all_fields_and_relations():
    current = build_test("old")
    updated = build_test("20 mg/L")
    (
        service,
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    ) = service_with_ports()
    test_port.get_test_by_id.return_value = current
    setup_valid_relations(
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    )
    test_port.update_test.return_value = current

    result = await service.update_test(str(TEST_ID), updated)

    assert result.result == "20 mg/L"
    assert result.test_type.id == TEST_TYPE_ID
    assert result.sample_id == str(SAMPLE_ID)
    assert result.analyte.id == ANALYTE_ID
    assert result.analysis_method.id == ANALYSIS_METHOD_ID
    assert result.criteria.id == CRITERIA_ID
    test_port.update_test.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_test_rejects_missing_item():
    service, test_port, *_ = service_with_ports()
    test_port.get_test_by_id.return_value = None

    with pytest.raises(MissingTestError):
        await service.update_test(str(TEST_ID), build_test())

    test_port.update_test.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_test_requires_existing_item():
    item = build_test()
    service, test_port, *_ = service_with_ports()
    test_port.get_test_by_id.return_value = item

    await service.delete_test(str(TEST_ID))

    test_port.delete_test.assert_awaited_once_with(str(TEST_ID))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("port_name", "exception"),
    [
        ("test_type_port", MissingTestTypeError),
        ("sample_port", SampleNotFoundError),
        ("analyte_port", AnalyteNotFoundError),
        ("analysis_method_port", AnalysisMethodNotFoundError),
        ("criteria_port", CriteriaNotFoundError),
    ],
)
async def test_create_test_rejects_missing_relations(port_name, exception):
    (
        service,
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    ) = service_with_ports()
    setup_valid_relations(
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    )
    ports = {
        "test_type_port": test_type_port.get_test_type_by_id,
        "sample_port": sample_port.get_sample_by_id,
        "analyte_port": analyte_port.get_analyte_by_id,
        "analysis_method_port": analysis_method_port.get_analysis_method_by_id,
        "criteria_port": criteria_port.get_criteria_by_id,
    }
    ports[port_name].return_value = None

    with pytest.raises(exception):
        await service.create_test(build_test())

    test_port.save_test.assert_not_awaited()


async def test_create_test_rejects_inconsistency_relations():
    (
        service,
        test_port,
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    ) = service_with_ports()
    setup_test_type_inconsistency(
        test_type_port,
        sample_port,
        analyte_port,
        analysis_method_port,
        criteria_port,
    )

    with pytest.raises(TestTypeConsistencyError):
        await service.create_test(build_test())

    test_port.save_test.assert_not_awaited()
