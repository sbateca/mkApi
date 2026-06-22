from pydantic import BaseModel, Field, field_validator

from application.dto.request.validators.sample_type_validators import (
    validate_sample_type_name,
)
from domain.util.str_functions import capitalize_str


class SampleTypeRequestDto(BaseModel):
    name: str = Field(max_length=150)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        capitalized_name = capitalize_str(value)
        return validate_sample_type_name(capitalized_name)
