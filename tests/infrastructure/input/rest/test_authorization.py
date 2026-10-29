from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from application.dto.response import SampleClientResponseDto
from domain.model.authenticated_user import AuthenticatedUser
from domain.util.constants import UserRole
from infrastructure.configuration.dependencies import get_sample_handler
from infrastructure.input.rest.security.authentication import get_authenticated_user
from main import app
from tests.infrastructure.input.rest.test_sample_controller import (
    SAMPLE_ID,
    sample_response,
)

USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")
CLIENT_ID = UUID("63cc2808-29d7-4c84-aa9f-feca7792a893")
OTHER_CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")


@pytest.mark.asyncio
async def test_client_only_receives_and_reads_own_samples():
    own_sample = sample_response().model_copy(
        update={"client": SampleClientResponseDto(id=CLIENT_ID, name="Own client")}
    )
    other_sample = sample_response().model_copy(
        update={
            "id": UUID("b64cd8b0-baad-4e63-9f5e-070633fd030e"),
            "client": SampleClientResponseDto(
                id=OTHER_CLIENT_ID,
                name="Other client",
            ),
        }
    )
    handler = AsyncMock()
    handler.get_samples.return_value = [own_sample, other_sample]
    handler.get_sample_by_id.side_effect = [own_sample, other_sample]
    app.dependency_overrides[get_authenticated_user] = lambda: AuthenticatedUser(
        USER_ID,
        frozenset({UserRole.CLIENT}),
        CLIENT_ID,
    )
    app.dependency_overrides[get_sample_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            listed = await client.get("/samples")
            own = await client.get(f"/samples/{SAMPLE_ID}")
            other = await client.get(f"/samples/{other_sample.id}")

        assert listed.status_code == 200
        assert [item["id"] for item in listed.json()] == [str(own_sample.id)]
        assert own.status_code == 200
        assert other.status_code == 403
    finally:
        app.dependency_overrides.pop(get_authenticated_user, None)
        app.dependency_overrides.pop(get_sample_handler, None)


@pytest.mark.asyncio
async def test_analyst_cannot_delete_samples():
    handler = AsyncMock()
    app.dependency_overrides[get_authenticated_user] = lambda: AuthenticatedUser(
        USER_ID,
        frozenset({UserRole.ANALYST}),
    )
    app.dependency_overrides[get_sample_handler] = lambda: handler

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.delete(f"/samples/{SAMPLE_ID}")

        assert response.status_code == 403
        handler.delete_sample.assert_not_awaited()
    finally:
        app.dependency_overrides.pop(get_authenticated_user, None)
        app.dependency_overrides.pop(get_sample_handler, None)
