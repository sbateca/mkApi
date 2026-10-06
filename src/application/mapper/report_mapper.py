from application.dto.request import GetReportByIdRequestDto, ReportRequestDto
from application.dto.response import ReportResponseDto
from application.mapper.sample_mapper import SampleMapper
from application.mapper.test_mapper import TestMapper
from domain.model.report import Report
from domain.model.sample import Sample
from domain.model.test import Test


class ReportMapper:
    def to_report(self, request: ReportRequestDto) -> Report:
        # Only relation IDs are needed; the use case resolves persisted objects.
        sample = Sample(
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
        tests = [
            Test(None, str(request.sample_id), None, None, None, "", id=test_id)
            for test_id in request.test_ids
        ]
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
