import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
@pytest.mark.parametrize("origin", ["http://localhost:5173", "http://localhost:5174"])
async def test_login_preflight_allows_frontend(origin):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.options(
            "/auth/login",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type,authorization",
            },
        )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert response.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_untrusted_origin_is_rejected():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.options(
            "/auth/login",
            headers={
                "Origin": "https://untrusted.example",
                "Access-Control-Request-Method": "POST",
            },
        )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


@pytest.mark.asyncio
async def test_validation_error_includes_cors_headers():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/auth/login", headers={"Origin": "http://localhost:5174"}, json={}
        )
    assert response.status_code == 422
    assert response.headers["access-control-allow-origin"] == "http://localhost:5174"


@pytest.mark.parametrize("in_use", [True, False])
async def test_sample_delete_errors_keep_cors_headers(in_use, monkeypatch):
    from unittest.mock import AsyncMock

    from domain.exception.sample_exception import SampleInUseError
    from infrastructure.configuration.dependencies import get_sample_handler
    from tests.builders.report_sample_builder import domain_sample

    handler = AsyncMock()
    handler.delete_sample.side_effect = (
        SampleInUseError() if in_use else RuntimeError("unexpected failure")
    )
    monkeypatch.setitem(app.dependency_overrides, get_sample_handler, lambda: handler)
    origin = "http://localhost:5173"

    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://test",
    ) as client:
        response = await client.delete(
            f"/samples/{domain_sample().id}", headers={"Origin": origin}
        )

    assert response.headers["access-control-allow-origin"] == origin
    assert response.status_code == (409 if in_use else 500)
    if in_use:
        assert response.json()["type"] == "SAMPLE_IN_USE"
