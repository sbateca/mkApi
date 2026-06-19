from abc import ABC, abstractmethod

from application.dto.request import (
    DeleteTestTypeRequestDto,
    GetTestTypeByIdRequestDto,
    TestTypeRequestDto,
    UpdateTestTypeRequestDto,
)
from application.dto.response import TestTypeResponseDto


class TestTypeHandlerInterface(ABC):
    @abstractmethod
    async def create_test_type(
        self, request: TestTypeRequestDto
    ) -> TestTypeResponseDto:
        pass

    @abstractmethod
    async def get_test_types(self) -> list[TestTypeResponseDto]:
        pass

    @abstractmethod
    async def get_test_type_by_id(
        self, request: GetTestTypeByIdRequestDto
    ) -> TestTypeResponseDto:
        pass

    @abstractmethod
    async def update_test_type(
        self, request: UpdateTestTypeRequestDto
    ) -> TestTypeResponseDto:
        pass

    @abstractmethod
    async def delete_test_type(self, request: DeleteTestTypeRequestDto) -> None:
        pass
