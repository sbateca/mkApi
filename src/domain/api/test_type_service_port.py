from abc import ABC, abstractmethod

from domain.model.test_type import TestType


class TestTypeServicePort(ABC):
    @abstractmethod
    async def create_test_type(self, test_type: TestType) -> TestType:
        pass

    @abstractmethod
    async def get_test_types(self) -> list[TestType]:
        pass

    @abstractmethod
    async def get_test_type_by_id(self, test_type_id: str) -> TestType:
        pass

    @abstractmethod
    async def update_test_type(
        self, test_type_id: str, updated_test_type: TestType
    ) -> TestType:
        pass

    @abstractmethod
    async def delete_test_type(self, test_type_id: str) -> None:
        pass
