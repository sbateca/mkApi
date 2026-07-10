from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import (
    AnalysisMethodResponseDto,
    AnalyteResponseDto,
    CriteriaResponseDto,
)
from application.dto.response import (
    TestResponseDto as ResponseDto,
)
from application.dto.response import (
    TestTypeResponseDto as TypeResponseDto,
)
from domain.exception.analysis_method_exception import AnalysisMethodNotFoundError
from domain.exception.analyte_exception import AnalyteNotFoundError
from domain.exception.criteria_exception import CriteriaNotFoundError
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_exception import TestNotFoundError as MissingTestError
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from infrastructure.configuration.dependencies import get_test_handler
from main import app

TEST_ID = UUID("a3c99dfc-b450-4d56-806a-449cb31d94a1")
TEST_TYPE_ID = UUID("2a4a260f-46ac-4efe-ad52-47db61e6d890")
SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
ANALYTE_ID = UUID("3871d51e-a6ed-479d-b94c-6803e5a7c538")
ANALYSIS_METHOD_ID = UUID("61c7e7ea-795a-4c9c-af23-99ba47556d2f")
CRITERIA_ID = UUID("122c8c5c-d55b-4ed7-ab70-266c6fcfb076")


def build_test_response() -> ResponseDto:
    test_type = TypeResponseDto(id=TEST_TYPE_ID, name="Physicochemical")
    return ResponseDto(
        id=TEST_ID,
        test_type=test_type,
        sample_id=str(SAMPLE_ID),
        analyte=AnalyteResponseDto(
            id=ANALYTE_ID,
            name="Chlorine",
            test_type=test_type,
        ),
        analysis_method=AnalysisMethodResponseDto(
            id=ANALYSIS_METHOD_ID,
            name="SM 4500",
        ),
        criteria=CriteriaResponseDto(id=CRITERIA_ID, name="Resolution 2115"),
        result="15 mg/L",
    )


def build_test_body() -> dict:
    return {
        "testTypeId": str(TEST_TYPE_ID),
        "sampleId": str(SAMPLE_ID),
        "analyteId": str(ANALYTE_ID),
        "analysisMethodId": str(ANALYSIS_METHOD_ID),
        "criteriaId": str(CRITERIA_ID),
        "result": "15 mg/L",
    }


def expected_response() -> dict:
    return {
        "id": str(TEST_ID),
        "testType": {
            "id": str(TEST_TYPE_ID),
            "name": "Physicochemical",
        },
        "sampleId": str(SAMPLE_ID),
        "analyte": {
            "id": str(ANALYTE_ID),
            "name": "Chlorine",
            "testType": {
                "id": str(TEST_TYPE_ID),
                "name": "Physicochemical",
            },
        },
        "analysisMethod": {
            "id": str(ANALYSIS_METHOD_ID),
            "name": "SM 4500",
        },
        "criteria": {
            "id": str(CRITERIA_ID),
            "name": "Resolution 2115",
        },
        "result": "15 mg/L",
    }


@pytest.mark.asyncio
async def test_test_crud_routes_delegate_to_handler_with_ui_shape():
    item = build_test_response()
    handler = AsyncMock()
    handler.create_test.return_value = item
    handler.get_tests.return_value = [item]
    handler.get_test_by_id.return_value = item
    handler.update_test.return_value = item
    handler.delete_test.return_value = None
    app.dependency_overrides[get_test_handler] = lambda: handler
    body = build_test_body()

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/tests", json=body)
            listed = await client.get("/tests")
            fetched = await client.get(f"/tests/{TEST_ID}")
            updated = await client.put(f"/tests/{TEST_ID}", json=body)
            deleted = await client.delete(f"/tests/{TEST_ID}")

        expected = expected_response()
        assert created.status_code == 201
        assert created.json() == expected
        assert listed.json() == [expected]
        assert fetched.json() == expected
        assert updated.json() == expected
        assert deleted.status_code == 204
        handler.create_test.assert_awaited_once()
        handler.get_tests.assert_awaited_once()
        handler.get_test_by_id.assert_awaited_once()
        handler.update_test.assert_awaited_once()
        handler.delete_test.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_test_routes_validate_body_and_path_ids():
    handler = AsyncMock()
    app.dependency_overrides[get_test_handler] = lambda: handler
    body = build_test_body()

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_result_body = {**body, "result": "  "}
            bad_analyte_body = {**body, "analyteId": "invalid"}
            blank_result = await client.post("/tests", json=blank_result_body)
            bad_analyte = await client.post("/tests", json=bad_analyte_body)
            bad_path = await client.get("/tests/invalid")

        assert blank_result.status_code == 422
        assert bad_analyte.status_code == 422
        assert bad_path.status_code == 422
        handler.create_test.assert_not_awaited()
        handler.get_test_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception", "status_code", "error_type"),
    [
        (MissingTestTypeError(), 404, "TEST_TYPE_NOT_FOUND"),
        (SampleNotFoundError(), 404, "SAMPLE_NOT_FOUND"),
        (AnalyteNotFoundError(), 404, "ANALYTE_NOT_FOUND"),
        (AnalysisMethodNotFoundError(), 404, "ANALYSIS_METHOD_NOT_FOUND"),
        (CriteriaNotFoundError(), 404, "CRITERIA_NOT_FOUND"),
    ],
)
async def test_create_test_maps_related_not_found_errors(
    exception, status_code, error_type
):
    handler = AsyncMock()
    handler.create_test.side_effect = exception
    app.dependency_overrides[get_test_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.post("/tests", json=build_test_body())

        assert result.status_code == status_code
        assert result.json()["type"] == error_type
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_test_maps_not_found_error():
    handler = AsyncMock()
    handler.get_test_by_id.side_effect = MissingTestError()
    app.dependency_overrides[get_test_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.get(f"/tests/{TEST_ID}")

        assert result.status_code == 404
        assert result.json()["type"] == "TEST_NOT_FOUND"
    finally:
        app.dependency_overrides.clear()
