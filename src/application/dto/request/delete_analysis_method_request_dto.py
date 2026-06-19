from pydantic import BaseModel, field_validator

from application.dto.request.validators.analysis_method_validators import (
    validate_analysis_method_id,
)


class DeleteAnalysisMethodRequestDto(BaseModel):
    analysis_method_id: str

    @field_validator("analysis_method_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_analysis_method_id(value)
