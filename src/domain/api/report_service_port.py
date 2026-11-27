from abc import ABC, abstractmethod

from domain.model.action_decision import ActionDecision
from domain.model.authenticated_user import AuthenticatedUser
from domain.model.report import Report, ReportWithActions


class ReportServicePort(ABC):
    @abstractmethod
    def get_create_decision(self, actor: AuthenticatedUser) -> ActionDecision:
        pass

    @abstractmethod
    async def get_reports(self, actor: AuthenticatedUser) -> list[ReportWithActions]:
        pass

    @abstractmethod
    async def get_report_by_id(
        self, report_id: str, actor: AuthenticatedUser
    ) -> ReportWithActions:
        pass

    @abstractmethod
    async def download_report(self, report_id: str, actor: AuthenticatedUser) -> bytes:
        pass

    @abstractmethod
    async def create_report(self, report: Report, actor: AuthenticatedUser) -> Report:
        pass

    @abstractmethod
    async def update_report(
        self, report_id: str, updated_report: Report, actor: AuthenticatedUser
    ) -> Report:
        pass

    @abstractmethod
    async def delete_report(self, report_id: str, actor: AuthenticatedUser) -> None:
        pass

    @abstractmethod
    async def set_report_status(
        self, report_id: str, status: str, actor: AuthenticatedUser
    ) -> Report:
        pass
