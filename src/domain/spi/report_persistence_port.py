from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.report import Report


class ReportPersistencePort(ABC):
    @abstractmethod
    async def save_report(self, report: Report) -> Report:
        pass

    @abstractmethod
    async def get_reports(self) -> list[Report]:
        pass

    @abstractmethod
    async def get_reports_by_client_id(self, client_id: UUID) -> list[Report]:
        pass

    @abstractmethod
    async def get_report_by_id(self, report_id: str) -> Report | None:
        pass

    @abstractmethod
    async def update_report(self, report: Report) -> Report:
        pass

    @abstractmethod
    async def delete_report(self, report_id: str) -> None:
        pass
