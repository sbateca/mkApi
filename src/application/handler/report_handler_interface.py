from abc import ABC, abstractmethod

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
from application.dto.response.report_response_dto import ReportWithActionsResponseDto
from domain.model.authenticated_user import AuthenticatedUser


class ReportHandlerInterface(ABC):
    @abstractmethod
    async def create_report(
        self, request: ReportRequestDto, actor: AuthenticatedUser
    ) -> ReportResponseDto:
        pass

    @abstractmethod
    async def get_reports(
        self, actor: AuthenticatedUser
    ) -> list[ReportWithActionsResponseDto]:
        pass

    @abstractmethod
    async def get_report_by_id(
        self, request: GetReportByIdRequestDto, actor: AuthenticatedUser
    ) -> ReportWithActionsResponseDto:
        pass

    @abstractmethod
    async def update_report(
        self, request: UpdateReportRequestDto, actor: AuthenticatedUser
    ) -> ReportResponseDto:
        pass

    @abstractmethod
    async def delete_report(
        self, request: DeleteReportRequestDto, actor: AuthenticatedUser
    ) -> None:
        pass

    @abstractmethod
    async def set_report_status(
        self, request: SetReportStatusRequestDto, actor: AuthenticatedUser
    ) -> ReportResponseDto:
        pass
