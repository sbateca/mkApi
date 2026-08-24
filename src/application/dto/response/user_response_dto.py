from uuid import UUID

from pydantic import BaseModel

from application.dto.response.role_response_dto import RoleResponseDto


class UserResponseDto(BaseModel):
    id: UUID | None
    name: str
    username: str
    email: str
    roles: list[RoleResponseDto]
