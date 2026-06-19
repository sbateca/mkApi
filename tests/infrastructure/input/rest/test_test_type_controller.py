from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import TestTypeResponseDto as TypeResponseDto
from domain.exception.test_type_exception import (
    TestTypeAlreadyExistsError as DuplicateTestTypeError,
)
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from infrastructure.configuration.dependencies import get_test_type_handler
from main import app

TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


@pytest.mark.asyncio
async def test_test_type_crud_routes_delegate_to_handler():
    response = TypeResponseDto(id=TEST_TYPE_ID, name="Physical-Chemical")
    handler = AsyncMock()
    handler.create_test_type.return_value = response
    handler.get_test_types.return_value = [response]
    handler.get_test_type_by_id.return_value = response
    handler.update_test_type.return_value = response
    handler.delete_test_type.return_value = None
    app.dependency_overrides[get_test_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post(
                "/test-types", json={"name": "Physical-Chemical"}
            )
            listed = await client.get("/test-types")
            fetched = await client.get(f"/test-types/{TEST_TYPE_ID}")
            updated = await client.put(
                f"/test-types/{TEST_TYPE_ID}",
                json={"name": "Physical-Chemical"},
            )
            deleted = await client.delete(f"/test-types/{TEST_TYPE_ID}")

        expected = {"id": str(TEST_TYPE_ID), "name": "Physical-Chemical"}
        assert created.status_code == 201
        assert created.json() == expected
        assert listed.json() == [expected]
        assert fetched.json() == expected
        assert updated.json() == expected
        assert deleted.status_code == 204
        handler.create_test_type.assert_awaited_once()
        handler.get_test_types.assert_awaited_once()
        handler.get_test_type_by_id.assert_awaited_once()
        handler.update_test_type.assert_awaited_once()
        handler.delete_test_type.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_test_type_routes_validate_blank_name_and_invalid_id():
    handler = AsyncMock()
    app.dependency_overrides[get_test_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_name = await client.post("/test-types", json={"name": "   "})
            invalid_id = await client.get("/test-types/not-a-uuid")

        assert blank_name.status_code == 422
        assert invalid_id.status_code == 422
        assert invalid_id.json()["errors"][0]["field"] == "test_type_id"
        handler.create_test_type.assert_not_awaited()
        handler.get_test_type_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_test_type_returns_conflict_for_duplicate_name():
    handler = AsyncMock()
    handler.create_test_type.side_effect = DuplicateTestTypeError()
    app.dependency_overrides[get_test_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.post(
                "/test-types", json={"name": "Physical-Chemical"}
            )

        assert result.status_code == 409
        assert result.json()["type"] == "TEST_TYPE_ALREADY_EXISTS"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_test_type_returns_not_found_for_missing_item():
    handler = AsyncMock()
    handler.get_test_type_by_id.side_effect = MissingTestTypeError()
    app.dependency_overrides[get_test_type_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.get(f"/test-types/{TEST_TYPE_ID}")

        assert result.status_code == 404
        assert result.json() == {
            "type": "TEST_TYPE_NOT_FOUND",
            "message": "The test type was not found.",
        }
    finally:
        app.dependency_overrides.clear()
