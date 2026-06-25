from pydantic import BaseModel, Field, field_validator

from application.dto.request.validators.common_validators import (
    validate_not_blank_value,
    validate_uuid,
)
from application.util.constants import AnalyteRequestError
from domain.util.str_functions import capitalize_str


class AnalyteRequestDto(BaseModel):
    name: str = Field(max_length=150)
    test_type_id: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        capitalized_name = capitalize_str(value)
        return validate_not_blank_value(
            capitalized_name, AnalyteRequestError.BLANK_NAME
        )

    @field_validator("test_type_id")
    @classmethod
    def validate_test_type_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            AnalyteRequestError.BLANK_TEST_TYPE_ID,
            AnalyteRequestError.INVALID_TEST_TYPE_ID,
        )
