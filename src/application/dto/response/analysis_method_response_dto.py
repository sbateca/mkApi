from uuid import UUID

from pydantic import BaseModel


class AnalysisMethodResponseDto(BaseModel):
    id: UUID | None
    name: str
