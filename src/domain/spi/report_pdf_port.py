from abc import ABC, abstractmethod

from domain.model.report import Report


class ReportPdfPort(ABC):
    @abstractmethod
    async def get_or_create(self, report: Report) -> bytes:
        pass
