from abc import ABC, abstractmethod

from application.dto.request import (
    CriteriaRequestDto,
    DeleteCriteriaRequestDto,
    GetCriteriaByIdRequestDto,
    UpdateCriteriaRequestDto,
)
from application.dto.response import CriteriaResponseDto


class CriteriaHandlerInterface(ABC):
    @abstractmethod
    async def create_criteria(self, request: CriteriaRequestDto) -> CriteriaResponseDto:
        pass

    @abstractmethod
    async def get_criteria(self) -> list[CriteriaResponseDto]:
        pass

    @abstractmethod
    async def get_criteria_by_id(
        self, request: GetCriteriaByIdRequestDto
    ) -> CriteriaResponseDto:
        pass

    @abstractmethod
    async def update_criteria(
        self, request: UpdateCriteriaRequestDto
    ) -> CriteriaResponseDto:
        pass

    @abstractmethod
    async def delete_criteria(self, request: DeleteCriteriaRequestDto) -> None:
        pass
