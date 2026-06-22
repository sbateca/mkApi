from uuid import UUID

from pydantic import BaseModel


class SampleTypeResponseDto(BaseModel):
    id: UUID | None
    name: str
