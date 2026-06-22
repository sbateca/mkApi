from pydantic import BaseModel, Field, field_validator

from application.dto.request.validators.analyte_validators import (
    validate_analyte_name,
    validate_analyte_test_type_id,
)
from domain.util.str_functions import capitalize_str


class AnalyteRequestDto(BaseModel):
    name: str = Field(max_length=150)
    test_type_id: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        capitalized_name = capitalize_str(value)
        return validate_analyte_name(capitalized_name)

    @field_validator("test_type_id")
    @classmethod
    def validate_test_type_id(cls, value: str) -> str:
        return validate_analyte_test_type_id(value)
