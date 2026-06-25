from abc import ABC, abstractmethod

from application.dto.request import (
    DeleteSampleRequestDto,
    GetSampleByIdRequestDto,
    SampleRequestDto,
    UpdateSampleRequestDto,
)
from application.dto.response import SampleResponseDto


class SampleHandlerInterface(ABC):
    @abstractmethod
    async def create_sample(self, request: SampleRequestDto) -> SampleResponseDto:
        pass

    @abstractmethod
    async def get_samples(self) -> list[SampleResponseDto]:
        pass

    @abstractmethod
    async def get_sample_by_id(
        self, request: GetSampleByIdRequestDto
    ) -> SampleResponseDto:
        pass

    @abstractmethod
    async def update_sample(self, request: UpdateSampleRequestDto) -> SampleResponseDto:
        pass

    @abstractmethod
    async def delete_sample(self, request: DeleteSampleRequestDto) -> None:
        pass
