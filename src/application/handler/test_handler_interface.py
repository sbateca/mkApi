from abc import ABC, abstractmethod

from application.dto.request import (
    DeleteTestRequestDto,
    GetTestByIdRequestDto,
    TestRequestDto,
    UpdateTestRequestDto,
)
from application.dto.response import TestResponseDto


class TestHandlerInterface(ABC):
    @abstractmethod
    async def create_test(self, request: TestRequestDto) -> TestResponseDto:
        pass

    @abstractmethod
    async def get_tests(self) -> list[TestResponseDto]:
        pass

    @abstractmethod
    async def get_test_by_id(self, request: GetTestByIdRequestDto) -> TestResponseDto:
        pass

    @abstractmethod
    async def update_test(self, request: UpdateTestRequestDto) -> TestResponseDto:
        pass

    @abstractmethod
    async def delete_test(self, request: DeleteTestRequestDto) -> None:
        pass
