from uuid import UUID

from pydantic import BaseModel


class CriteriaResponseDto(BaseModel):
    id: UUID | None
    name: str
