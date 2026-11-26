from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID


class ReportTestPersistencePort(ABC):
    @abstractmethod
    async def save_report_tests(
        self, report_id: UUID, test_ids: Sequence[UUID]
    ) -> None:
        """Insert ordered links within the caller’s transaction."""
        pass
