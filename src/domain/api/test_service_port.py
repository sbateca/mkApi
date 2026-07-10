from abc import ABC, abstractmethod

from domain.model.test import Test


class TestServicePort(ABC):
    @abstractmethod
    async def get_tests(self) -> list[Test]:
        pass

    @abstractmethod
    async def get_test_by_id(self, test_id: str) -> Test:
        pass

    @abstractmethod
    async def create_test(self, test: Test) -> Test:
        pass

    @abstractmethod
    async def update_test(self, test_id: str, updated_test: Test) -> Test:
        pass

    @abstractmethod
    async def delete_test(self, test_id: str) -> None:
        pass
