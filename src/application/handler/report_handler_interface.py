from abc import ABC, abstractmethod

from application.dto.request import (
    DeleteReportRequestDto,
    GetReportByIdRequestDto,
    ReportRequestDto,
    UpdateReportRequestDto,
)
from application.dto.response import ReportResponseDto
from src.application.dto.request.set_report_status_request_dto import (
    SetReportStatusRequestDto,
)


class ReportHandlerInterface(ABC):
    @abstractmethod
    async def create_report(self, request: ReportRequestDto) -> ReportResponseDto:
        pass

    @abstractmethod
    async def get_reports(self) -> list[ReportResponseDto]:
        pass

    @abstractmethod
    async def get_report_by_id(
        self, request: GetReportByIdRequestDto
    ) -> ReportResponseDto:
        pass

    @abstractmethod
    async def update_report(self, request: UpdateReportRequestDto) -> ReportResponseDto:
        pass

    @abstractmethod
    async def delete_report(self, request: DeleteReportRequestDto) -> None:
        pass

    @abstractmethod
    async def set_report_status(
        self, request: SetReportStatusRequestDto
    ) -> ReportResponseDto:
        pass
