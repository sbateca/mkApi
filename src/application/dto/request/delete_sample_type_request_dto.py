from pydantic import BaseModel, field_validator

from application.dto.request.validators.sample_type_validators import (
    validate_sample_type_id,
)


class DeleteSampleTypeRequestDto(BaseModel):
    sample_type_id: str

    @field_validator("sample_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_sample_type_id(value)
