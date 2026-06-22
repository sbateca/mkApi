from pydantic import BaseModel, Field, field_validator

from application.dto.request.validators.test_type_validators import (
    validate_test_type_name,
)
from domain.util.str_functions import capitalize_str


class TestTypeRequestDto(BaseModel):
    name: str = Field(max_length=150)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = capitalize_str(value)
        return validate_test_type_name(value)
