from pydantic import BaseModel, field_validator

from application.dto.request.validators.test_type_validators import (
    validate_test_type_id,
)


class GetTestTypeByIdRequestDto(BaseModel):
    test_type_id: str

    @field_validator("test_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_test_type_id(value)
