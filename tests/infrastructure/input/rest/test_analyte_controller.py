from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import AnalyteResponseDto
from application.dto.response import TestTypeResponseDto as TypeResponseDto
from domain.exception.analyte_exception import (
    AnalyteAlreadyExistsError as DuplicateAnalyteError,
)
from domain.exception.analyte_exception import (
    AnalyteNotFoundError as MissingAnalyteError,
)
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from infrastructure.configuration.dependencies import get_analyte_handler
from main import app

ANALYTE_ID = UUID("7dc56aee-5530-4df9-896f-c63d8d39f28e")
TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


def response() -> AnalyteResponseDto:
    return AnalyteResponseDto(
        id=ANALYTE_ID,
        name="pH",
        test_type=TypeResponseDto(id=TEST_TYPE_ID, name="Physical-Chemical"),
    )


@pytest.mark.asyncio
async def test_analyte_crud_routes_delegate_to_handler():
    item = response()
    handler = AsyncMock()
    handler.create_analyte.return_value = item
    handler.get_analytes.return_value = [item]
    handler.get_analyte_by_id.return_value = item
    handler.update_analyte.return_value = item
    handler.delete_analyte.return_value = None
    app.dependency_overrides[get_analyte_handler] = lambda: handler
    body = {"name": "pH", "test_type_id": str(TEST_TYPE_ID)}

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/analytes", json=body)
            listed = await client.get("/analytes")
            fetched = await client.get(f"/analytes/{ANALYTE_ID}")
            updated = await client.put(f"/analytes/{ANALYTE_ID}", json=body)
            deleted = await client.delete(f"/analytes/{ANALYTE_ID}")

        expected = {
            "id": str(ANALYTE_ID),
            "name": "pH",
            "test_type": {
                "id": str(TEST_TYPE_ID),
                "name": "Physical-Chemical",
            },
        }
        assert created.status_code == 201
        assert created.json() == expected
        assert listed.json() == [expected]
        assert fetched.json() == expected
        assert updated.json() == expected
        assert deleted.status_code == 204
        handler.create_analyte.assert_awaited_once()
        handler.get_analytes.assert_awaited_once()
        handler.get_analyte_by_id.assert_awaited_once()
        handler.update_analyte.assert_awaited_once()
        handler.delete_analyte.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_analyte_routes_validate_body_and_path_ids():
    handler = AsyncMock()
    app.dependency_overrides[get_analyte_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_name = await client.post(
                "/analytes",
                json={"name": "  ", "test_type_id": str(TEST_TYPE_ID)},
            )
            bad_test_type = await client.post(
                "/analytes", json={"name": "pH", "test_type_id": "invalid"}
            )
            bad_path = await client.get("/analytes/invalid")

        assert blank_name.status_code == 422
        assert bad_test_type.status_code == 422
        assert bad_path.status_code == 422
        handler.create_analyte.assert_not_awaited()
        handler.get_analyte_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception", "status_code", "error_type"),
    [
        (DuplicateAnalyteError(), 409, "ANALYTE_ALREADY_EXISTS"),
        (MissingTestTypeError(), 404, "TEST_TYPE_NOT_FOUND"),
    ],
)
async def test_create_analyte_maps_domain_errors(exception, status_code, error_type):
    handler = AsyncMock()
    handler.create_analyte.side_effect = exception
    app.dependency_overrides[get_analyte_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.post(
                "/analytes",
                json={"name": "pH", "test_type_id": str(TEST_TYPE_ID)},
            )

        assert result.status_code == status_code
        assert result.json()["type"] == error_type
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_analyte_maps_not_found_error():
    handler = AsyncMock()
    handler.get_analyte_by_id.side_effect = MissingAnalyteError()
    app.dependency_overrides[get_analyte_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.get(f"/analytes/{ANALYTE_ID}")

        assert result.status_code == 404
        assert result.json()["type"] == "ANALYTE_NOT_FOUND"
    finally:
        app.dependency_overrides.clear()
