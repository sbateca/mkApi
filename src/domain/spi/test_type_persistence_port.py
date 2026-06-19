from abc import ABC, abstractmethod

from domain.model.test_type import TestType


class TestTypePersistencePort(ABC):
    @abstractmethod
    async def save_test_type(self, test_type: TestType) -> TestType:
        pass

    @abstractmethod
    async def get_test_types(self) -> list[TestType]:
        pass

    @abstractmethod
    async def get_test_type_by_id(self, test_type_id: str) -> TestType | None:
        pass

    @abstractmethod
    async def get_test_type_by_name(self, name: str) -> TestType | None:
        pass

    @abstractmethod
    async def get_test_type_by_name_excluding_id(
        self, name: str, test_type_id: str
    ) -> TestType | None:
        pass

    @abstractmethod
    async def update_test_type(self, test_type: TestType) -> TestType:
        pass

    @abstractmethod
    async def delete_test_type(self, test_type_id: str) -> None:
        pass
