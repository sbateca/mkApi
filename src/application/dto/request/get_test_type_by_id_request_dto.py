from pydantic import BaseModel, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import TestTypeRequestError


class GetTestTypeByIdRequestDto(BaseModel):
    test_type_id: str

    @field_validator("test_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestTypeRequestError.BLANK_TEST_TYPE_ID,
            TestTypeRequestError.INVALID_TEST_TYPE_ID,
        )
