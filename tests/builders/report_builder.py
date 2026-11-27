from dataclasses import replace
from datetime import date
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_scope import AuthorizationScope
from domain.model.report import Report
from domain.policy.action_policy import ActionPolicy
from domain.usecase.report_use_case import ReportUseCase
from domain.util.constants import UserRole
from tests.builders.report_sample_builder import (
    domain_sample,
)
from tests.builders.report_test_builder import (
    domain_test,
)


def admin():
    return AuthenticatedUser(uuid4(), frozenset({UserRole.ADMIN}))


def body():
    test = domain_test()
    return {
        "reportNumber": "FE 3157 - 361",
        "reportDate": "2024-08-05",
        "status": "draft",
        "sampleId": str(domain_sample().id),
        "testIds": [
            {
                "id": str(test.id),
                "testTypeId": str(test.test_type.id),
                "analysisMethodId": str(test.analysis_method.id),
                "analyteId": str(test.analyte.id),
                "criteriaId": str(test.criteria.id),
                "result": test.result,
                "sampleId": str(domain_sample().id),
            }
        ],
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
    reports, samples, tests, authorization = (
        AsyncMock(),
        AsyncMock(),
        AsyncMock(),
        Mock(),
    )
    authorization.get_scope.return_value = AuthorizationScope.ALL
    samples.get_sample_by_id.return_value = domain_sample()
    authorization.is_allowed.return_value = True
    test = domain_test()
    tests.save_test.side_effect = lambda item: item
    reports.save_report.side_effect = lambda item, *, report_tests_port: item
    reports.update_report.side_effect = lambda item: item
    reports.update_report_status.side_effect = lambda report_id, status: replace(
        reports.get_report_by_id.return_value, status=status
    )
    return (
        ReportUseCase(
            report_persistence_port=reports,
            report_pdf_port=AsyncMock(
                get_or_create=AsyncMock(return_value=b"%PDF-test")
            ),
            sample_persistence_port=samples,
            analyte_persistence_port=AsyncMock(
                get_analyte_by_id=AsyncMock(return_value=test.analyte)
            ),
            analysis_method_persistence_port=AsyncMock(
                get_analysis_method_by_id=AsyncMock(return_value=test.analysis_method)
            ),
            criteria_persistence_port=AsyncMock(
                get_criteria_by_id=AsyncMock(return_value=test.criteria)
            ),
            test_type_persistence_port=AsyncMock(
                get_test_type_by_id=AsyncMock(return_value=test.test_type)
            ),
            report_test_persistence_port=AsyncMock(),
            authorization_port=authorization,
            action_policy=ActionPolicy(authorization),
        ),
        reports,
        samples,
        tests,
    )
