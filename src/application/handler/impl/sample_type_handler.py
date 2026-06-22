from application.dto.request import (
    DeleteSampleTypeRequestDto,
    GetSampleTypeByIdRequestDto,
    SampleTypeRequestDto,
    UpdateSampleTypeRequestDto,
)
from application.dto.response import SampleTypeResponseDto
from application.handler.sample_type_handler_interface import SampleTypeHandlerInterface
from application.mapper.sample_type_mapper import SampleTypeMapper
from domain.api.sample_type_service_port import SampleTypeServicePort


class SampleTypeHandler(SampleTypeHandlerInterface):
    def __init__(self, mapper: SampleTypeMapper, service: SampleTypeServicePort):
        self.mapper = mapper
        self.service = service

    async def create_sample_type(
        self, request: SampleTypeRequestDto
    ) -> SampleTypeResponseDto:
        created = await self.service.create_sample_type(
            self.mapper.to_sample_type(request)
        )
        return self.mapper.to_response(created)

    async def get_sample_types(self) -> list[SampleTypeResponseDto]:
        return self.mapper.to_response_list(await self.service.get_sample_types())

    async def get_sample_type_by_id(
        self, request: GetSampleTypeByIdRequestDto
    ) -> SampleTypeResponseDto:
        sample_type = await self.service.get_sample_type_by_id(
            self.mapper.to_sample_type_id(request)
        )
        return self.mapper.to_response(sample_type)

    async def update_sample_type(
        self, request: UpdateSampleTypeRequestDto
    ) -> SampleTypeResponseDto:
        updated = await self.service.update_sample_type(
            request.sample_type_id,
            self.mapper.to_sample_type(request.sample_type),
        )
        return self.mapper.to_response(updated)

    async def delete_sample_type(self, request: DeleteSampleTypeRequestDto) -> None:
        await self.service.delete_sample_type(request.sample_type_id)
