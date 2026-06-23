from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import CriteriaResponseDto
from domain.exception.criteria_exception import (
    CriteriaAlreadyExistsError as DuplicateCriteriaError,
)
from domain.exception.criteria_exception import (
    CriteriaNotFoundError as MissingCriteriaError,
)
from infrastructure.configuration.dependencies import get_criteria_handler
from main import app

CRITERIA_ID = UUID("b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3")


@pytest.mark.asyncio
async def test_criteria_crud_routes_delegate_to_handler():
    response = CriteriaResponseDto(id=CRITERIA_ID, name="0 UFC/100 ml")
    handler = AsyncMock()
    handler.create_criteria.return_value = response
    handler.get_criteria.return_value = [response]
    handler.get_criteria_by_id.return_value = response
    handler.update_criteria.return_value = response
    handler.delete_criteria.return_value = None
    app.dependency_overrides[get_criteria_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/criteria", json={"name": "0 UFC/100 ml"})
            listed = await client.get("/criteria")
            fetched = await client.get(f"/criteria/{CRITERIA_ID}")
            updated = await client.put(
                f"/criteria/{CRITERIA_ID}",
                json={"name": "0 UFC/100 ml"},
            )
            deleted = await client.delete(f"/criteria/{CRITERIA_ID}")

        expected = {"id": str(CRITERIA_ID), "name": "0 UFC/100 ml"}
        assert created.status_code == 201
        assert created.json() == expected
        assert listed.json() == [expected]
        assert fetched.json() == expected
        assert updated.json() == expected
        assert deleted.status_code == 204
        handler.create_criteria.assert_awaited_once()
        handler.get_criteria.assert_awaited_once()
        handler.get_criteria_by_id.assert_awaited_once()
        handler.update_criteria.assert_awaited_once()
        handler.delete_criteria.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_criteria_routes_validate_blank_name_and_invalid_id():
    handler = AsyncMock()
    app.dependency_overrides[get_criteria_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_name = await client.post("/criteria", json={"name": "   "})
            invalid_id = await client.get("/criteria/not-a-uuid")

        assert blank_name.status_code == 422
        assert invalid_id.status_code == 422
        assert invalid_id.json()["errors"][0]["field"] == "criteria_id"
        handler.create_criteria.assert_not_awaited()
        handler.get_criteria_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception", "status_code", "error_type"),
    [
        (DuplicateCriteriaError(), 409, "CRITERIA_ALREADY_EXISTS"),
        (MissingCriteriaError(), 404, "CRITERIA_NOT_FOUND"),
    ],
)
async def test_criteria_routes_map_domain_errors(exception, status_code, error_type):
    handler = AsyncMock()
    handler.create_criteria.side_effect = exception
    app.dependency_overrides[get_criteria_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.post("/criteria", json={"name": "0 UFC/100 ml"})

        assert result.status_code == status_code
        assert result.json()["type"] == error_type
    finally:
        app.dependency_overrides.clear()
