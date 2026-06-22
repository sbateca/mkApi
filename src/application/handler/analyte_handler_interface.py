from abc import ABC, abstractmethod

from application.dto.request import (
    AnalyteRequestDto,
    DeleteAnalyteRequestDto,
    GetAnalyteByIdRequestDto,
    UpdateAnalyteRequestDto,
)
from application.dto.response import AnalyteResponseDto


class AnalyteHandlerInterface(ABC):
    @abstractmethod
    async def create_analyte(self, request: AnalyteRequestDto) -> AnalyteResponseDto:
        pass

    @abstractmethod
    async def get_analytes(self) -> list[AnalyteResponseDto]:
        pass

    @abstractmethod
    async def get_analyte_by_id(
        self, request: GetAnalyteByIdRequestDto
    ) -> AnalyteResponseDto:
        pass

    @abstractmethod
    async def update_analyte(
        self, request: UpdateAnalyteRequestDto
    ) -> AnalyteResponseDto:
        pass

    @abstractmethod
    async def delete_analyte(self, request: DeleteAnalyteRequestDto) -> None:
        pass
