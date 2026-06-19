from uuid import UUID

from pydantic import BaseModel


class TestTypeResponseDto(BaseModel):
    id: UUID | None
    name: str
