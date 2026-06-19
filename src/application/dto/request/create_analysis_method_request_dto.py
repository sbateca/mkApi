from pydantic import BaseModel, Field, field_validator

from application.dto.request.validators.analysis_method_validators import (
    validate_analysis_method_name,
)


class AnalysisMethodRequestDto(BaseModel):
    name: str = Field(max_length=150)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_analysis_method_name(value)
