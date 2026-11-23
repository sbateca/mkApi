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
