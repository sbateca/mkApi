from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import TestRequestError


class GetTestByIdRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    test_id: str = Field(alias="testId")

    @field_validator("test_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestRequestError.BLANK_TEST_ID,
            TestRequestError.INVALID_TEST_ID,
        )
