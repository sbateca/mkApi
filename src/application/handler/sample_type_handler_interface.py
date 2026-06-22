from abc import ABC, abstractmethod

from application.dto.request import (
    DeleteSampleTypeRequestDto,
    GetSampleTypeByIdRequestDto,
    SampleTypeRequestDto,
    UpdateSampleTypeRequestDto,
)
from application.dto.response import SampleTypeResponseDto


class SampleTypeHandlerInterface(ABC):
    @abstractmethod
    async def create_sample_type(
        self, request: SampleTypeRequestDto
    ) -> SampleTypeResponseDto:
        pass

    @abstractmethod
    async def get_sample_types(self) -> list[SampleTypeResponseDto]:
        pass

    @abstractmethod
    async def get_sample_type_by_id(
        self, request: GetSampleTypeByIdRequestDto
    ) -> SampleTypeResponseDto:
        pass

    @abstractmethod
    async def update_sample_type(
        self, request: UpdateSampleTypeRequestDto
    ) -> SampleTypeResponseDto:
        pass

    @abstractmethod
    async def delete_sample_type(self, request: DeleteSampleTypeRequestDto) -> None:
        pass
