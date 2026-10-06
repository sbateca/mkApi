from abc import ABC, abstractmethod

from domain.model.report import Report


class ReportServicePort(ABC):
    @abstractmethod
    async def get_reports(self) -> list[Report]:
        pass

    @abstractmethod
    async def get_report_by_id(self, report_id: str) -> Report:
        pass

    @abstractmethod
    async def create_report(self, report: Report) -> Report:
        pass

    @abstractmethod
    async def update_report(self, report_id: str, updated_report: Report) -> Report:
        pass

    @abstractmethod
    async def delete_report(self, report_id: str) -> None:
        pass

    @abstractmethod
    async def set_report_status(self, report_id: str, status: str) -> Report:
        pass
