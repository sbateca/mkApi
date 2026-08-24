from abc import ABC, abstractmethod

from application.dto.request.user_request_dto import (
    UpdateUserRequestDto,
    UserIdRequestDto,
    UserRequestDto,
)
from application.dto.response.user_response_dto import UserResponseDto


class UserHandlerInterface(ABC):
    @abstractmethod
    async def create_user(self, request: UserRequestDto) -> UserResponseDto: ...
    @abstractmethod
    async def get_users(self) -> list[UserResponseDto]: ...
    @abstractmethod
    async def get_user(self, request: UserIdRequestDto) -> UserResponseDto: ...
    @abstractmethod
    async def update_user(self, request: UpdateUserRequestDto) -> UserResponseDto: ...
    @abstractmethod
    async def delete_user(self, request: UserIdRequestDto) -> None: ...
