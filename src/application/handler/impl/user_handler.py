from application.dto.request.user_request_dto import (
    UpdateUserRequestDto,
    UserIdRequestDto,
    UserRequestDto,
)
from application.dto.response.user_response_dto import UserResponseDto
from application.handler.user_handler_interface import UserHandlerInterface
from application.mapper.user_mapper import UserMapper
from domain.api.user_service_port import UserServicePort


class UserHandler(UserHandlerInterface):
    def __init__(self, mapper: UserMapper, service: UserServicePort):
        self.mapper, self.service = mapper, service

    async def create_user(self, request: UserRequestDto) -> UserResponseDto:
        return self.mapper.to_response(
            await self.service.create_user(self.mapper.to_domain(request))
        )

    async def get_users(self) -> list[UserResponseDto]:
        return self.mapper.to_response_list(await self.service.get_users())

    async def get_user(self, request: UserIdRequestDto) -> UserResponseDto:
        return self.mapper.to_response(
            await self.service.get_user_by_id(request.user_id)
        )

    async def update_user(self, request: UpdateUserRequestDto) -> UserResponseDto:
        user = await self.service.update_user(
            request.user_id, self.mapper.to_domain(request.user)
        )
        return self.mapper.to_response(user)

    async def delete_user(self, request: UserIdRequestDto) -> None:
        await self.service.delete_user(request.user_id)
