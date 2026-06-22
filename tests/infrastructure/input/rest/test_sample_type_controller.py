from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import SampleTypeResponseDto as TypeResponseDto
from domain.exception.sample_type_exception import (
    SampleTypeAlreadyExistsError as DuplicateSampleTypeError,
)
from domain.exception.sample_type_exception import (
    SampleTypeNotFoundError as MissingSampleTypeError,
)
from infrastructure.configuration.dependencies import get_sample_type_handler
from main import app

SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")


@pytest.mark.asyncio
async def test_sample_type_crud_routes_delegate_to_handler():
    response = TypeResponseDto(id=SAMPLE_TYPE_ID, name="Bottled water")
    handler = AsyncMock()
    handler.create_sample_type.return_value = response
    handler.get_sample_types.return_value = [response]
    handler.get_sample_type_by_id.return_value = response
    handler.update_sample_type.return_value = response
    handler.delete_sample_type.return_value = None
    app.dependency_overrides[get_sample_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/sample-types", json={"name": "Bottled water"})
            listed = await client.get("/sample-types")
            fetched = await client.get(f"/sample-types/{SAMPLE_TYPE_ID}")
            updated = await client.put(
                f"/sample-types/{SAMPLE_TYPE_ID}",
                json={"name": "Bottled water"},
            )
            deleted = await client.delete(f"/sample-types/{SAMPLE_TYPE_ID}")

        expected = {"id": str(SAMPLE_TYPE_ID), "name": "Bottled water"}
        assert created.status_code == 201
        assert created.json() == expected
        assert listed.json() == [expected]
        assert fetched.json() == expected
        assert updated.json() == expected
        assert deleted.status_code == 204
        handler.create_sample_type.assert_awaited_once()
        handler.get_sample_types.assert_awaited_once()
        handler.get_sample_type_by_id.assert_awaited_once()
        handler.update_sample_type.assert_awaited_once()
        handler.delete_sample_type.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sample_type_routes_validate_blank_name_and_invalid_id():
    handler = AsyncMock()
    app.dependency_overrides[get_sample_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_name = await client.post("/sample-types", json={"name": "   "})
            invalid_id = await client.get("/sample-types/not-a-uuid")

        assert blank_name.status_code == 422
        assert invalid_id.status_code == 422
        assert invalid_id.json()["errors"][0]["field"] == "sample_type_id"
        handler.create_sample_type.assert_not_awaited()
        handler.get_sample_type_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception", "status_code", "error_type"),
    [
        (DuplicateSampleTypeError(), 409, "SAMPLE_TYPE_ALREADY_EXISTS"),
        (MissingSampleTypeError(), 404, "SAMPLE_TYPE_NOT_FOUND"),
    ],
)
async def test_sample_type_routes_map_domain_errors(exception, status_code, error_type):
    handler = AsyncMock()
    handler.create_sample_type.side_effect = exception
    app.dependency_overrides[get_sample_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.post("/sample-types", json={"name": "Bottled water"})

        assert result.status_code == status_code
        assert result.json()["type"] == error_type
    finally:
        app.dependency_overrides.clear()
