from pydantic import BaseModel, Field, field_validator

from application.dto.request.validators.common_validators import (
    validate_not_blank_value,
)
from application.util.constants import SampleTypeRequestError
from domain.util.str_functions import capitalize_str


class SampleTypeRequestDto(BaseModel):
    name: str = Field(max_length=150)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        capitalized_name = capitalize_str(value)
        return validate_not_blank_value(
            capitalized_name,
            SampleTypeRequestError.BLANK_NAME,
        )
