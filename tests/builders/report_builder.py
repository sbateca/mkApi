from datetime import date
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.model.report import Report
from domain.usecase.report_use_case import ReportUseCase
from tests.builders.report_sample_builder import (
    domain_sample,
)
from tests.builders.report_test_builder import (
    domain_test,
)


def body():
    return {
        "reportNumber": "FE 3157 - 361",
        "reportDate": "2024-08-05",
        "status": "draft",
        "sampleId": str(domain_sample().id),
        "testIds": [str(domain_test().id)],
    }


def report():
    return Report(
        "FE 3157 - 361",
        date(2024, 8, 5),
        "draft",
        domain_sample(),
        [domain_test()],
        uuid4(),
    )


def service():
    reports, samples, tests = AsyncMock(), AsyncMock(), AsyncMock()
    samples.get_sample_by_id.return_value = domain_sample()
    tests.get_test_by_id.return_value = domain_test()
    reports.save_report.side_effect = lambda item: item
    reports.update_report.side_effect = lambda item: item
    return ReportUseCase(reports, samples, tests), reports, samples, tests
