from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from application.dto.response.test_type_response_dto import TestTypeResponseDto


class AnalyteResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID | None
    name: str
    test_type: TestTypeResponseDto = Field(serialization_alias="testType")
