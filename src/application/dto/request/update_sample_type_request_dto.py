from pydantic import BaseModel, field_validator

from application.dto.request.create_sample_type_request_dto import (
    SampleTypeRequestDto,
)
from application.dto.request.validators.sample_type_validators import (
    validate_sample_type_id,
)
from domain.util.str_functions import capitalize_str


class UpdateSampleTypeRequestDto(BaseModel):
    sample_type_id: str
    sample_type: SampleTypeRequestDto

    @field_validator("sample_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        capitalized_name = capitalize_str(value)
        return validate_sample_type_id(capitalized_name)
