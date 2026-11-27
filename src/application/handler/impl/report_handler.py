from application.dto.request import (
    DeleteReportRequestDto,
    GetReportByIdRequestDto,
    ReportRequestDto,
    UpdateReportRequestDto,
)
from application.dto.request.set_report_status_request_dto import (
    SetReportStatusRequestDto,
)
from application.dto.response import ReportResponseDto
from application.dto.response.action_response_dto import ActionDecisionResponseDto
from application.dto.response.report_response_dto import (
    ReportCollectionActionsResponseDto,
    ReportWithActionsResponseDto,
)
from application.handler.report_handler_interface import ReportHandlerInterface
from application.mapper.report_mapper import ReportMapper
from domain.api.report_service_port import ReportServicePort
from domain.model.authenticated_user import AuthenticatedUser


class ReportHandler(ReportHandlerInterface):
    def __init__(self, mapper: ReportMapper, service: ReportServicePort):
        self.mapper = mapper
        self.service = service

    def get_collection_actions(
        self, actor: AuthenticatedUser
    ) -> ReportCollectionActionsResponseDto:
        decision = self.service.get_create_decision(actor)
        return ReportCollectionActionsResponseDto(
            create=ActionDecisionResponseDto.from_decision(decision)
        )

    async def create_report(
        self, request: ReportRequestDto, actor: AuthenticatedUser
    ) -> ReportResponseDto:
        created = await self.service.create_report(
            self.mapper.to_report(request), actor
        )
        return self.mapper.to_response(created)

    async def get_reports(
        self, actor: AuthenticatedUser
    ) -> list[ReportWithActionsResponseDto]:
        return self.mapper.to_response_list_with_actions(
            await self.service.get_reports(actor)
        )

    async def get_report_by_id(
        self, request: GetReportByIdRequestDto, actor: AuthenticatedUser
    ) -> ReportWithActionsResponseDto:
        report = await self.service.get_report_by_id(
            self.mapper.to_report_id(request), actor
        )
        return self.mapper.to_response_with_actions(report)

    async def download_report(
        self, request: GetReportByIdRequestDto, actor: AuthenticatedUser
    ) -> bytes:
        return await self.service.download_report(
            self.mapper.to_report_id(request), actor
        )

    async def update_report(
        self, request: UpdateReportRequestDto, actor: AuthenticatedUser
    ) -> ReportResponseDto:
        updated = await self.service.update_report(
            request.report_id, self.mapper.to_report(request.report), actor
        )
        return self.mapper.to_response(updated)

    async def delete_report(
        self, request: DeleteReportRequestDto, actor: AuthenticatedUser
    ) -> None:
        await self.service.delete_report(request.report_id, actor)

    async def set_report_status(
        self, request: SetReportStatusRequestDto, actor: AuthenticatedUser
    ) -> ReportResponseDto:
        updated_report = await self.service.set_report_status(
            request.report_id, request.status, actor
        )
        return self.mapper.to_response(updated_report)
