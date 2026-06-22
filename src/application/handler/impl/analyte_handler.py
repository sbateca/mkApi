from application.dto.request import (
    AnalyteRequestDto,
    DeleteAnalyteRequestDto,
    GetAnalyteByIdRequestDto,
    UpdateAnalyteRequestDto,
)
from application.dto.response import AnalyteResponseDto
from application.handler.analyte_handler_interface import AnalyteHandlerInterface
from application.mapper.analyte_mapper import AnalyteMapper
from domain.api.analyte_service_port import AnalyteServicePort


class AnalyteHandler(AnalyteHandlerInterface):
    def __init__(self, mapper: AnalyteMapper, service: AnalyteServicePort):
        self.mapper = mapper
        self.service = service

    async def create_analyte(self, request: AnalyteRequestDto) -> AnalyteResponseDto:
        created = await self.service.create_analyte(self.mapper.to_analyte(request))
        return self.mapper.to_response(created)

    async def get_analytes(self) -> list[AnalyteResponseDto]:
        return self.mapper.to_response_list(await self.service.get_analytes())

    async def get_analyte_by_id(
        self, request: GetAnalyteByIdRequestDto
    ) -> AnalyteResponseDto:
        analyte = await self.service.get_analyte_by_id(
            self.mapper.to_analyte_id(request)
        )
        return self.mapper.to_response(analyte)

    async def update_analyte(
        self, request: UpdateAnalyteRequestDto
    ) -> AnalyteResponseDto:
        updated = await self.service.update_analyte(
            request.analyte_id, self.mapper.to_analyte(request.analyte)
        )
        return self.mapper.to_response(updated)

    async def delete_analyte(self, request: DeleteAnalyteRequestDto) -> None:
        await self.service.delete_analyte(request.analyte_id)
