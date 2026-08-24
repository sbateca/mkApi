from uuid import UUID

from pydantic import BaseModel

from domain.util.constants import UserRole


class RoleResponseDto(BaseModel):
    id: UUID | None
    name: UserRole
