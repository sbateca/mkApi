from uuid import UUID

from pydantic import BaseModel

from application.dto.response.test_type_response_dto import TestTypeResponseDto


class AnalyteResponseDto(BaseModel):
    id: UUID | None
    name: str
    test_type: TestTypeResponseDto
