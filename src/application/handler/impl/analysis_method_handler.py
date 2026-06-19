from application.dto.request import (
    AnalysisMethodRequestDto,
    DeleteAnalysisMethodRequestDto,
    GetAnalysisMethodByIdRequestDto,
    UpdateAnalysisMethodRequestDto,
)
from application.dto.response import AnalysisMethodResponseDto
from application.handler.analysis_method_handler_interface import (
    AnalysisMethodHandlerInterface,
)
from application.mapper.analysis_method_mapper import AnalysisMethodMapper
from domain.api.analysis_method_service_port import AnalysisMethodServicePort


class AnalysisMethodHandler(AnalysisMethodHandlerInterface):
    def __init__(
        self,
        analysis_method_mapper: AnalysisMethodMapper,
        analysis_method_service_port: AnalysisMethodServicePort,
    ):
        self.analysis_method_mapper = analysis_method_mapper
        self.analysis_method_service_port = analysis_method_service_port

    async def create_analysis_method(
        self, request: AnalysisMethodRequestDto
    ) -> AnalysisMethodResponseDto:
        analysis_method = self.analysis_method_mapper.to_analysis_method(request)
        created = await self.analysis_method_service_port.create_analysis_method(
            analysis_method
        )
        return self.analysis_method_mapper.to_response(created)

    async def get_analysis_methods(self) -> list[AnalysisMethodResponseDto]:
        analysis_methods = (
            await self.analysis_method_service_port.get_analysis_methods()
        )
        return self.analysis_method_mapper.to_response_list(analysis_methods)

    async def get_analysis_method_by_id(
        self, request: GetAnalysisMethodByIdRequestDto
    ) -> AnalysisMethodResponseDto:
        analysis_method_id = self.analysis_method_mapper.to_analysis_method_id(request)
        analysis_method = (
            await self.analysis_method_service_port.get_analysis_method_by_id(
                analysis_method_id
            )
        )
        return self.analysis_method_mapper.to_response(analysis_method)

    async def update_analysis_method(
        self, request: UpdateAnalysisMethodRequestDto
    ) -> AnalysisMethodResponseDto:
        analysis_method = self.analysis_method_mapper.to_analysis_method(
            request.analysis_method
        )
        updated = await self.analysis_method_service_port.update_analysis_method(
            request.analysis_method_id,
            analysis_method,
        )
        return self.analysis_method_mapper.to_response(updated)

    async def delete_analysis_method(
        self, request: DeleteAnalysisMethodRequestDto
    ) -> None:
        await self.analysis_method_service_port.delete_analysis_method(
            request.analysis_method_id
        )
