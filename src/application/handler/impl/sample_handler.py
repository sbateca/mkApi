from application.dto.request import (
    DeleteSampleRequestDto,
    GetSampleByIdRequestDto,
    SampleRequestDto,
    UpdateSampleRequestDto,
)
from application.dto.response import SampleResponseDto
from application.handler.sample_handler_interface import SampleHandlerInterface
from application.mapper.sample_mapper import SampleMapper
from domain.api.sample_service_port import SampleServicePort


class SampleHandler(SampleHandlerInterface):
    def __init__(self, mapper: SampleMapper, service: SampleServicePort):
        self.mapper = mapper
        self.service = service

    async def create_sample(self, request: SampleRequestDto) -> SampleResponseDto:
        created = await self.service.create_sample(self.mapper.to_sample(request))
        return self.mapper.to_response(created)

    async def get_samples(self) -> list[SampleResponseDto]:
        return self.mapper.to_response_list(await self.service.get_samples())

    async def get_sample_by_id(
        self, request: GetSampleByIdRequestDto
    ) -> SampleResponseDto:
        sample = await self.service.get_sample_by_id(self.mapper.to_sample_id(request))
        return self.mapper.to_response(sample)

    async def update_sample(self, request: UpdateSampleRequestDto) -> SampleResponseDto:
        updated = await self.service.update_sample(
            request.sample_id,
            self.mapper.to_sample(request.sample),
        )
        return self.mapper.to_response(updated)

    async def delete_sample(self, request: DeleteSampleRequestDto) -> None:
        await self.service.delete_sample(request.sample_id)
