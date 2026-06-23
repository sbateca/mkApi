from abc import ABC, abstractmethod

from domain.model.criteria import Criteria


class CriteriaServicePort(ABC):
    @abstractmethod
    async def create_criteria(self, criteria: Criteria) -> Criteria:
        pass

    @abstractmethod
    async def get_criteria(self) -> list[Criteria]:
        pass

    @abstractmethod
    async def get_criteria_by_id(self, criteria_id: str) -> Criteria:
        pass

    @abstractmethod
    async def update_criteria(
        self, criteria_id: str, updated_criteria: Criteria
    ) -> Criteria:
        pass

    @abstractmethod
    async def delete_criteria(self, criteria_id: str) -> None:
        pass
