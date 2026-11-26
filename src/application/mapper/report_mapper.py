from application.dto.request import GetReportByIdRequestDto, ReportRequestDto
from application.dto.response.report_response_dto import (
    ActionDecisionResponseDto,
    ReportResponseDto,
    ReportWithActionsResponseDto,
)
from application.mapper.sample_mapper import SampleMapper
from application.mapper.test_mapper import TestMapper
from domain.model.report import Report, ReportWithActions
from domain.model.sample import Sample
from domain.model.test import Test
from src.domain.model.analysis_method import AnalysisMethod
from src.domain.model.analyte import Analyte
from src.domain.model.criteria import Criteria
from src.domain.model.test_type import TestType


class ReportMapper:
    def to_report(self, request: ReportRequestDto) -> Report:
        sample = self.to_sample(request)
        tests = self.to_tests(request)
        return Report(
            request.report_number, request.report_date, request.status, sample, tests
        )

    def to_response(self, report: Report) -> ReportResponseDto:
        return ReportResponseDto(
            id=report.id,
            report_number=report.report_number,
            report_date=report.report_date,
            status=report.status,
            sample=SampleMapper().to_response(report.sample),
            tests=TestMapper().to_response_list(report.tests),
        )

    def to_response_list(self, reports: list[Report]) -> list[ReportResponseDto]:
        return [self.to_response(report) for report in reports]

    def to_report_id(self, request: GetReportByIdRequestDto) -> str:
        return request.report_id

    def to_response_with_actions(
        self, report: ReportWithActions
    ) -> ReportWithActionsResponseDto:
        return ReportWithActionsResponseDto(
            id=report.id,
            report_number=report.report_number,
            report_date=report.report_date,
            status=report.status,
            sample=SampleMapper().to_response(report.sample),
            tests=TestMapper().to_response_list(report.tests),
            actions={
                action: ActionDecisionResponseDto(
                    allowed=decision.allowed,
                    code=decision.code,
                    reason=decision.reason,
                )
                for action, decision in report.actions.items()
            },
        )

    def to_response_list_with_actions(
        self, reports: list[ReportWithActions]
    ) -> list[ReportWithActionsResponseDto]:
        return [self.to_response_with_actions(report) for report in reports]

    def to_sample(self, request: ReportRequestDto) -> Sample:
        return Sample(
            sample_code="",
            sample_type=None,
            client=None,
            get_sample_date=request.report_date,
            reception_date=request.report_date,
            analysis_date=request.report_date,
            sample_location="",
            responsable="",
            id=request.sample_id,
        )

    def to_tests(self, request: ReportRequestDto) -> list[Test]:
        return [
            Test(
                id=test.id,
                sample_id=str(request.sample_id),
                test_type=TestType(id=test.test_type_id, name=None),
                analysis_method=AnalysisMethod(id=test.analysis_method_id, name=None),
                analyte=Analyte(
                    id=test.analyte_id,
                    name=None,
                    test_type=TestType(id=test.test_type_id, name=None),
                ),
                criteria=Criteria(id=test.criteria_id, name=None),
                result=test.result,
            )
            for test in request.test_ids
        ]
