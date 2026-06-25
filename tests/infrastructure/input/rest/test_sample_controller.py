from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import (
    SampleClientResponseDto,
    SampleResponseDto,
    SampleTypeSummaryResponseDto,
)
from domain.exception.client_exception import ClientNotFoundError as MissingClientError
from domain.exception.sample_exception import (
    SampleAlreadyExistsError as DuplicateSampleError,
)
from domain.exception.sample_exception import SampleNotFoundError as MissingSampleError
from domain.exception.sample_type_exception import (
    SampleTypeNotFoundError as MissingSampleTypeError,
)
from infrastructure.configuration.dependencies import get_sample_handler
from main import app

SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")
CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")


def sample_response() -> SampleResponseDto:
    return SampleResponseDto(
        id=SAMPLE_ID,
        sample_code="1001",
        sample_type=SampleTypeSummaryResponseDto(
            id=SAMPLE_TYPE_ID,
            name="Bottled water",
        ),
        client=SampleClientResponseDto(id=CLIENT_ID, name="Maximum Hotel"),
        get_sample_date=date(2024, 7, 2),
        reception_date=date(2023, 10, 1),
        analysis_date=date(2023, 10, 2),
        sample_location="Hotel's restaurant",
        responsable="John Lenon",
    )


def sample_body() -> dict:
    return {
        "sampleCode": "1001",
        "sampleTypeId": str(SAMPLE_TYPE_ID),
        "clientId": str(CLIENT_ID),
        "getSampleDate": "2024-07-02",
        "receptionDate": "2023-10-01",
        "analysisDate": "2023-10-02",
        "sampleLocation": "Hotel's restaurant",
        "responsable": "John Lenon",
    }


def expected_response() -> dict:
    return {
        "id": str(SAMPLE_ID),
        "sampleCode": "1001",
        "sampleType": {
            "id": str(SAMPLE_TYPE_ID),
            "name": "Bottled water",
        },
        "client": {
            "id": str(CLIENT_ID),
            "name": "Maximum Hotel",
        },
        "getSampleDate": "2024-07-02",
        "receptionDate": "2023-10-01",
        "analysisDate": "2023-10-02",
        "sampleLocation": "Hotel's restaurant",
        "responsable": "John Lenon",
    }


@pytest.mark.asyncio
async def test_sample_crud_routes_delegate_to_handler_with_ui_shape():
    item = sample_response()
    handler = AsyncMock()
    handler.create_sample.return_value = item
    handler.get_samples.return_value = [item]
    handler.get_sample_by_id.return_value = item
    handler.update_sample.return_value = item
    handler.delete_sample.return_value = None
    app.dependency_overrides[get_sample_handler] = lambda: handler
    body = sample_body()

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/samples", json=body)
            listed = await client.get("/samples")
            fetched = await client.get(f"/samples/{SAMPLE_ID}")
            updated = await client.put(f"/samples/{SAMPLE_ID}", json=body)
            deleted = await client.delete(f"/samples/{SAMPLE_ID}")

        expected = expected_response()
        assert created.status_code == 201
        assert created.json() == expected
        assert listed.json() == [expected]
        assert fetched.json() == expected
        assert updated.json() == expected
        assert deleted.status_code == 204
        handler.create_sample.assert_awaited_once()
        handler.get_samples.assert_awaited_once()
        handler.get_sample_by_id.assert_awaited_once()
        handler.update_sample.assert_awaited_once()
        handler.delete_sample.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sample_routes_validate_body_and_path_ids():
    handler = AsyncMock()
    app.dependency_overrides[get_sample_handler] = lambda: handler
    body = sample_body()

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            blank_code_body = {**body, "sampleCode": "  "}
            bad_sample_type_body = {**body, "sampleTypeId": "invalid"}
            blank_code = await client.post("/samples", json=blank_code_body)
            bad_sample_type = await client.post("/samples", json=bad_sample_type_body)
            bad_path = await client.get("/samples/invalid")

        assert blank_code.status_code == 422
        assert bad_sample_type.status_code == 422
        assert bad_path.status_code == 422
        handler.create_sample.assert_not_awaited()
        handler.get_sample_by_id.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception", "status_code", "error_type"),
    [
        (DuplicateSampleError(), 409, "SAMPLE_ALREADY_EXISTS"),
        (MissingSampleTypeError(), 404, "SAMPLE_TYPE_NOT_FOUND"),
        (MissingClientError(), 404, "CLIENT_NOT_FOUND"),
    ],
)
async def test_create_sample_maps_domain_errors(exception, status_code, error_type):
    handler = AsyncMock()
    handler.create_sample.side_effect = exception
    app.dependency_overrides[get_sample_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.post("/samples", json=sample_body())

        assert result.status_code == status_code
        assert result.json()["type"] == error_type
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_sample_maps_not_found_error():
    handler = AsyncMock()
    handler.get_sample_by_id.side_effect = MissingSampleError()
    app.dependency_overrides[get_sample_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            result = await client.get(f"/samples/{SAMPLE_ID}")

        assert result.status_code == 404
        assert result.json()["type"] == "SAMPLE_NOT_FOUND"
    finally:
        app.dependency_overrides.clear()
