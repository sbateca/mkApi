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
            assert (
                await client.patch(f"/reports/{item.id}/approve")
            ).status_code == 200
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
