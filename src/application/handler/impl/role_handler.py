from application.dto.request.role_request_dto import (
    RoleIdRequestDto,
    RoleRequestDto,
    UpdateRoleRequestDto,
)
from application.dto.response.role_response_dto import RoleResponseDto
from application.handler.role_handler_interface import RoleHandlerInterface
from application.mapper.role_mapper import RoleMapper
from domain.api.role_service_port import RoleServicePort


class RoleHandler(RoleHandlerInterface):
    def __init__(self, mapper: RoleMapper, service: RoleServicePort):
        self.mapper, self.service = mapper, service

    async def create_role(self, request: RoleRequestDto) -> RoleResponseDto:
        return self.mapper.to_response(
            await self.service.create_role(self.mapper.to_domain(request))
        )

    async def get_roles(self) -> list[RoleResponseDto]:
        return self.mapper.to_response_list(await self.service.get_roles())

    async def get_role(self, request: RoleIdRequestDto) -> RoleResponseDto:
        return self.mapper.to_response(
            await self.service.get_role_by_id(request.role_id)
        )

    async def update_role(self, request: UpdateRoleRequestDto) -> RoleResponseDto:
        role = await self.service.update_role(
            request.role_id, self.mapper.to_domain(request.role)
        )
        return self.mapper.to_response(role)

    async def delete_role(self, request: RoleIdRequestDto) -> None:
        await self.service.delete_role(request.role_id)
