from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request import (
    DeleteTestRequestDto,
    GetTestByIdRequestDto,
    UpdateTestRequestDto,
)
from application.dto.request import (
    TestRequestDto as RequestDto,
)
from application.handler.impl.test_handler import TestHandler as AppHandler
from application.mapper.test_mapper import TestMapper as AppMapper
from domain.model.analysis_method import AnalysisMethod as DomainAnalysisMethod
from domain.model.analyte import Analyte as DomainAnalyte
from domain.model.criteria import Criteria as DomainCriteria
from domain.model.test import Test as DomainTest
from domain.model.test_type import TestType as DomainTestType

TEST_ID = UUID("a3c99dfc-b450-4d56-806a-449cb31d94a1")
TEST_TYPE_ID = UUID("2a4a260f-46ac-4efe-ad52-47db61e6d890")
SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
ANALYTE_ID = UUID("3871d51e-a6ed-479d-b94c-6803e5a7c538")
ANALYSIS_METHOD_ID = UUID("61c7e7ea-795a-4c9c-af23-99ba47556d2f")
CRITERIA_ID = UUID("122c8c5c-d55b-4ed7-ab70-266c6fcfb076")


def build_test_body() -> RequestDto:
    return RequestDto(
        testTypeId=str(TEST_TYPE_ID),
        sampleId=str(SAMPLE_ID),
        analyteId=str(ANALYTE_ID),
        analysisMethodId=str(ANALYSIS_METHOD_ID),
        criteriaId=str(CRITERIA_ID),
        result="15 mg/L",
    )


def build_domain_test() -> DomainTest:
    test_type = DomainTestType(id=TEST_TYPE_ID, name="Physicochemical")
    return DomainTest(
        id=TEST_ID,
        test_type=test_type,
        sample_id=str(SAMPLE_ID),
        analyte=DomainAnalyte(
            id=ANALYTE_ID,
            name="Chlorine",
            test_type=test_type,
        ),
        analysis_method=DomainAnalysisMethod(id=ANALYSIS_METHOD_ID, name="SM 4500"),
        criteria=DomainCriteria(id=CRITERIA_ID, name="Resolution 2115"),
        result="15 mg/L",
    )


def test_test_mapper_maps_request_domain_and_nested_response():
    mapper = AppMapper()
    request = build_test_body()
    domain = build_domain_test()

    mapped = mapper.to_test(request)
    response = mapper.to_response(domain)
    dumped = response.model_dump(by_alias=True)

    assert mapped.id is None
    assert mapped.test_type.id == TEST_TYPE_ID
    assert mapped.sample_id == str(SAMPLE_ID)
    assert mapped.analyte.id == ANALYTE_ID
    assert mapped.analysis_method.id == ANALYSIS_METHOD_ID
    assert mapped.criteria.id == CRITERIA_ID
    assert response.id == TEST_ID
    assert response.test_type.name == "Physicochemical"
    assert response.analyte.name == "Chlorine"
    assert response.analysis_method.name == "SM 4500"
    assert response.criteria.name == "Resolution 2115"
    assert dumped["testType"]["name"] == "Physicochemical"
    assert dumped["sampleId"] == str(SAMPLE_ID)
    assert dumped["analysisMethod"]["name"] == "SM 4500"
    assert mapper.to_response_list([domain]) == [response]
    assert mapper.to_test_id(GetTestByIdRequestDto(testId=str(TEST_ID))) == str(TEST_ID)


@pytest.mark.asyncio
async def test_test_handler_delegates_all_operations():
    domain = build_domain_test()
    service = AsyncMock()
    service.create_test.return_value = domain
    service.get_tests.return_value = [domain]
    service.get_test_by_id.return_value = domain
    service.update_test.return_value = domain
    handler = AppHandler(AppMapper(), service)
    body = build_test_body()

    assert (await handler.create_test(body)).id == TEST_ID
    assert len(await handler.get_tests()) == 1
    assert (
        await handler.get_test_by_id(GetTestByIdRequestDto(testId=str(TEST_ID)))
    ).id == TEST_ID
    assert (
        await handler.update_test(UpdateTestRequestDto(testId=str(TEST_ID), test=body))
    ).id == TEST_ID
    assert await handler.delete_test(DeleteTestRequestDto(testId=str(TEST_ID))) is None

    service.create_test.assert_awaited_once()
    service.get_tests.assert_awaited_once()
    service.get_test_by_id.assert_awaited_once_with(str(TEST_ID))
    service.update_test.assert_awaited_once()
    service.delete_test.assert_awaited_once_with(str(TEST_ID))
