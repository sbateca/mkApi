from abc import ABC, abstractmethod

from application.dto.request import (
    AnalysisMethodRequestDto,
    DeleteAnalysisMethodRequestDto,
    GetAnalysisMethodByIdRequestDto,
    UpdateAnalysisMethodRequestDto,
)
from application.dto.response import AnalysisMethodResponseDto


class AnalysisMethodHandlerInterface(ABC):
    @abstractmethod
    async def create_analysis_method(
        self, request: AnalysisMethodRequestDto
    ) -> AnalysisMethodResponseDto:
        pass

    @abstractmethod
    async def get_analysis_methods(self) -> list[AnalysisMethodResponseDto]:
        pass

    @abstractmethod
    async def get_analysis_method_by_id(
        self, request: GetAnalysisMethodByIdRequestDto
    ) -> AnalysisMethodResponseDto:
        pass

    @abstractmethod
    async def update_analysis_method(
        self, request: UpdateAnalysisMethodRequestDto
    ) -> AnalysisMethodResponseDto:
        pass

    @abstractmethod
    async def delete_analysis_method(
        self, request: DeleteAnalysisMethodRequestDto
    ) -> None:
        pass
