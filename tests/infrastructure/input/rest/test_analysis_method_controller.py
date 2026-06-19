from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import AnalysisMethodResponseDto
from infrastructure.configuration.dependencies import get_analysis_method_handler
from main import app

ANALYSIS_METHOD_ID = UUID("c461270c-6682-4f51-9148-efb9fbaab44e")


@pytest.mark.asyncio
async def test_analysis_method_crud_routes_delegate_to_handler():
    response = AnalysisMethodResponseDto(id=ANALYSIS_METHOD_ID, name="NTC")
    handler = AsyncMock()
    handler.create_analysis_method.return_value = response
    handler.get_analysis_methods.return_value = [response]
    handler.get_analysis_method_by_id.return_value = response
    handler.update_analysis_method.return_value = response
    handler.delete_analysis_method.return_value = None
    app.dependency_overrides[get_analysis_method_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/analysis-methods", json={"name": "NTC"})
            listed = await client.get("/analysis-methods")
            fetched = await client.get(f"/analysis-methods/{ANALYSIS_METHOD_ID}")
            updated = await client.put(
                f"/analysis-methods/{ANALYSIS_METHOD_ID}", json={"name": "NTC"}
            )
            deleted = await client.delete(f"/analysis-methods/{ANALYSIS_METHOD_ID}")

        assert created.status_code == 201
        assert created.json() == {"id": str(ANALYSIS_METHOD_ID), "name": "NTC"}
        assert listed.json() == [created.json()]
        assert fetched.json() == created.json()
        assert updated.json() == created.json()
        assert deleted.status_code == 204
        handler.create_analysis_method.assert_awaited_once()
        handler.get_analysis_methods.assert_awaited_once()
        handler.get_analysis_method_by_id.assert_awaited_once()
        handler.update_analysis_method.assert_awaited_once()
        handler.delete_analysis_method.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_analysis_method_routes_validate_name_and_id():
    handler = AsyncMock()
    app.dependency_overrides[get_analysis_method_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_name = await client.post("/analysis-methods", json={"name": "   "})
            invalid_id = await client.get("/analysis-methods/not-a-uuid")

        assert blank_name.status_code == 422
        assert invalid_id.status_code == 422
        assert invalid_id.json()["errors"][0]["field"] == "analysis_method_id"
        handler.create_analysis_method.assert_not_awaited()
        handler.get_analysis_method_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()
