from application.dto.request import (
    CriteriaRequestDto,
    DeleteCriteriaRequestDto,
    GetCriteriaByIdRequestDto,
    UpdateCriteriaRequestDto,
)
from application.dto.response import CriteriaResponseDto
from application.handler.criteria_handler_interface import CriteriaHandlerInterface
from application.mapper.criteria_mapper import CriteriaMapper
from domain.api.criteria_service_port import CriteriaServicePort


class CriteriaHandler(CriteriaHandlerInterface):
    def __init__(self, mapper: CriteriaMapper, service: CriteriaServicePort):
        self.mapper = mapper
        self.service = service

    async def create_criteria(self, request: CriteriaRequestDto) -> CriteriaResponseDto:
        created = await self.service.create_criteria(self.mapper.to_criteria(request))
        return self.mapper.to_response(created)

    async def get_criteria(self) -> list[CriteriaResponseDto]:
        return self.mapper.to_response_list(await self.service.get_criteria())

    async def get_criteria_by_id(
        self, request: GetCriteriaByIdRequestDto
    ) -> CriteriaResponseDto:
        criteria = await self.service.get_criteria_by_id(
            self.mapper.to_criteria_id(request)
        )
        return self.mapper.to_response(criteria)

    async def update_criteria(
        self, request: UpdateCriteriaRequestDto
    ) -> CriteriaResponseDto:
        updated = await self.service.update_criteria(
            request.criteria_id,
            self.mapper.to_criteria(request.criteria),
        )
        return self.mapper.to_response(updated)

    async def delete_criteria(self, request: DeleteCriteriaRequestDto) -> None:
        await self.service.delete_criteria(request.criteria_id)
