from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import TestTypeRequestError


class DeleteTestTypeRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    test_type_id: str = Field(alias="testTypeId")

    @field_validator("test_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestTypeRequestError.BLANK_TEST_TYPE_ID,
            TestTypeRequestError.INVALID_TEST_TYPE_ID,
        )
