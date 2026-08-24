from abc import ABC, abstractmethod

from application.dto.request.role_request_dto import (
    RoleIdRequestDto,
    RoleRequestDto,
    UpdateRoleRequestDto,
)
from application.dto.response.role_response_dto import RoleResponseDto


class RoleHandlerInterface(ABC):
    @abstractmethod
    async def create_role(self, request: RoleRequestDto) -> RoleResponseDto: ...
    @abstractmethod
    async def get_roles(self) -> list[RoleResponseDto]: ...
    @abstractmethod
    async def get_role(self, request: RoleIdRequestDto) -> RoleResponseDto: ...
    @abstractmethod
    async def update_role(self, request: UpdateRoleRequestDto) -> RoleResponseDto: ...
    @abstractmethod
    async def delete_role(self, request: RoleIdRequestDto) -> None: ...
