from application.dto.request import (
    DeleteReportRequestDto,
    GetReportByIdRequestDto,
    ReportRequestDto,
    UpdateReportRequestDto,
)
from application.dto.response import ReportResponseDto
from application.handler.report_handler_interface import ReportHandlerInterface
from application.mapper.report_mapper import ReportMapper
from domain.api.report_service_port import ReportServicePort
from src.application.dto.request import set_report_status_request_dto


class ReportHandler(ReportHandlerInterface):
    def __init__(self, mapper: ReportMapper, service: ReportServicePort):
        self.mapper = mapper
        self.service = service

    async def create_report(self, request: ReportRequestDto) -> ReportResponseDto:
        created = await self.service.create_report(self.mapper.to_report(request))
        return self.mapper.to_response(created)

    async def get_reports(self) -> list[ReportResponseDto]:
        return self.mapper.to_response_list(await self.service.get_reports())

    async def get_report_by_id(
        self, request: GetReportByIdRequestDto
    ) -> ReportResponseDto:
        report = await self.service.get_report_by_id(self.mapper.to_report_id(request))
        return self.mapper.to_response(report)

    async def update_report(self, request: UpdateReportRequestDto) -> ReportResponseDto:
        updated = await self.service.update_report(
            request.report_id,
            self.mapper.to_report(request.report),
        )
        return self.mapper.to_response(updated)

    async def delete_report(self, request: DeleteReportRequestDto) -> None:
        await self.service.delete_report(request.report_id)

    async def set_report_status(
        self, request: set_report_status_request_dto
    ) -> ReportResponseDto:
        updated_report = await self.service.set_report_status(
            request.report_id, request.status
        )
        return self.mapper.to_response(updated_report)
