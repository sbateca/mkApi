from httpx import ASGITransport, AsyncClient

from application.handler.impl.report_handler import ReportHandler
from application.mapper.report_mapper import ReportMapper
from domain.model.authorization_action import AuthorizationAction
from domain.util.constants import ResourceType
from infrastructure.configuration.dependencies import get_report_handler
from infrastructure.input.rest.security.authentication import get_authenticated_user
from main import app
from tests.builders.report_builder import body, report, service
from tests.builders.report_sample_builder import domain_sample
from tests.builders.report_test_builder import domain_test


async def test_report_routes_with_real_handler_and_mapper():
    usecase, persistence, _, _ = service()
    item = report()
    persistence.get_report_by_id.return_value = item
    persistence.get_reports.return_value = [item]
    app.dependency_overrides[get_report_handler] = lambda: ReportHandler(
        ReportMapper(), usecase
    )
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            created = await client.post("/reports", json=body())
            assert created.status_code == 201
            data = created.json()
            assert data["reportNumber"] == body()["reportNumber"]
            assert data["status"] == "draft"
            assert data["sample"]["client"]["name"] == domain_sample().client.name
            assert (
                data["tests"][0]["analyte"]["testType"]["name"]
                == domain_test().test_type.name
            )
            actor = app.dependency_overrides[get_authenticated_user]()
            response = await client.get("/reports")
            assert response.json()[0]["id"] == str(item.id)
            usecase.authorization_port.get_scope.assert_called_with(
                actor,
                AuthorizationAction.READ,
                ResourceType.REPORT,
            )
            assert (await client.get(f"/reports/{item.id}")).status_code == 200
            assert (
                await client.put(f"/reports/{item.id}", json=body())
            ).status_code == 200
            approved = await client.patch(f"/reports/{item.id}/approve")
            assert approved.status_code == 200
            assert approved.json()["status"] == "approved"
            assert (await client.delete(f"/reports/{item.id}")).status_code == 204
            for method in [client.get, client.delete]:
                assert (await method("/reports/invalid")).status_code == 422
            assert (
                await client.put("/reports/invalid", json=body())
            ).status_code == 422
            assert (
                await client.post("/reports", json=body() | {"testIds": ["bad"]})
            ).status_code == 422
            persistence.get_report_by_id.return_value = None
            response = await client.get(f"/reports/{item.id}")
            assert response.status_code == 404
            assert response.json()["type"] == "REPORT_NOT_FOUND"
    finally:
        app.dependency_overrides.pop(get_report_handler, None)


async def test_report_usecase_injects_links_with_the_report_session():
    from typing import Annotated
    from unittest.mock import AsyncMock

    from fastapi import Depends, FastAPI

    from domain.usecase.report_use_case import ReportUseCase
    from infrastructure.configuration.dependencies import (
        get_db_session,
        get_report_usecase,
    )

    probe = FastAPI()
    session = AsyncMock()
    probe.dependency_overrides[get_db_session] = lambda: session

    @probe.get("/")
    async def check_usecase(
        service: Annotated[ReportUseCase, Depends(get_report_usecase)],
    ):
        assert service.report_test_persistence_port.session is session
        assert service.report_persistence_port.repository.session is session
        return {"injected": True}

    async with AsyncClient(
        transport=ASGITransport(app=probe), base_url="http://test"
    ) as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"injected": True}


async def test_collection_actions_reports_create_permission_without_listing_reports():
    from domain.model.authenticated_user import AuthenticatedUser
    from domain.util.constants import UserRole

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        original_actor = app.dependency_overrides[get_authenticated_user]
        try:
            for role in UserRole:
                app.dependency_overrides[get_authenticated_user] = lambda role=role: (
                    AuthenticatedUser(id=original_actor().id, roles=frozenset({role}))
                )
                response = await client.get("/reports/actions")
                assert response.status_code == 200
                allowed = role in {
                    UserRole.ADMIN,
                    UserRole.TECHNICAL_DIRECTOR,
                    UserRole.ANALYST,
                }
                decision = response.json()["create"]
                assert decision["allowed"] is allowed
                assert decision["code"] == (None if allowed else "forbidden")
                if not allowed:
                    assert (
                        await client.post("/reports", json=body())
                    ).status_code == 403
        finally:
            app.dependency_overrides[get_authenticated_user] = original_actor


async def test_download_authorizes_before_generating_and_returns_pdf(monkeypatch):
    from unittest.mock import Mock

    from domain.exception.report_exception import ReportPdfUnavailableError
    from infrastructure.configuration.dependencies import get_report_usecase
    from infrastructure.output.pdf.report_pdf_adapter import ReportPdfAdapter

    usecase, persistence, _, _ = service()
    item = report()
    persistence.get_report_by_id.return_value = item
    storage = Mock()
    storage.get_or_create.side_effect = lambda key, generate: generate()
    usecase.report_pdf_port = ReportPdfAdapter(storage)
    monkeypatch.setitem(app.dependency_overrides, get_report_usecase, lambda: usecase)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        url = f"/reports/{item.id}/download"
        denied = await client.get(url)
        assert denied.status_code == 403
        storage.get_or_create.assert_not_called()

        item.status = "approved"
        response = await client.get(url)
        storage.get_or_create.side_effect = ReportPdfUnavailableError()
        unavailable = await client.get(url)

    assert unavailable.status_code == 503
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"] == (
        f'attachment; filename="reporte-{item.id}.pdf"'
    )
    assert response.content.startswith(b"%PDF-")
    assert storage.get_or_create.call_args.args[0] == f"reports/v2/{item.id}.pdf"
