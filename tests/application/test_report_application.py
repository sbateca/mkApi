import pytest
from pydantic import ValidationError

from application.dto.request import ReportRequestDto
from tests.builders.report_builder import body
from tests.builders.report_test_builder import domain_test


@pytest.mark.parametrize(
    "change",
    [
        {"reportNumber": " "},
        {"status": " "},
        {"sampleId": "invalid"},
        {"reportDate": "bad"},
        {"testIds": ["bad"]},
        {"testIds": [str(domain_test().id)] * 2},
    ],
)
def test_report_request_validation(change):
    with pytest.raises(ValidationError):
        ReportRequestDto(**(body() | change))


async def test_status_handler_delegates_and_maps_response():
    from unittest.mock import AsyncMock

    from application.dto.request.set_report_status_request_dto import (
        SetReportStatusRequestDto,
    )
    from application.handler.impl.report_handler import ReportHandler
    from application.mapper.report_mapper import ReportMapper
    from tests.builders.report_builder import report

    item = report()
    item.status = "Approved"
    service = AsyncMock()
    service.set_report_status.return_value = item
    handler = ReportHandler(ReportMapper(), service)
    request = SetReportStatusRequestDto(reportId=str(item.id), status="Approved")
    response = await handler.set_report_status(request)
    service.set_report_status.assert_awaited_once_with(str(item.id), "Approved")
    assert response.id == item.id
    assert response.status == "Approved"
    assert response.sample.id == item.sample.id
    assert response.tests[0].id == item.tests[0].id
