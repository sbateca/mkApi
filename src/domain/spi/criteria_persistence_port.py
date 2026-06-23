from abc import ABC, abstractmethod

from domain.model.criteria import Criteria


class CriteriaPersistencePort(ABC):
    @abstractmethod
    async def save_criteria(self, criteria: Criteria) -> Criteria:
        pass

    @abstractmethod
    async def get_criteria(self) -> list[Criteria]:
        pass

    @abstractmethod
    async def get_criteria_by_id(self, criteria_id: str) -> Criteria | None:
        pass

    @abstractmethod
    async def get_criteria_by_name(self, name: str) -> Criteria | None:
        pass

    @abstractmethod
    async def get_criteria_by_name_excluding_id(
        self, name: str, criteria_id: str
    ) -> Criteria | None:
        pass

    @abstractmethod
    async def update_criteria(self, criteria: Criteria) -> Criteria:
        pass

    @abstractmethod
    async def delete_criteria(self, criteria_id: str) -> None:
        pass
