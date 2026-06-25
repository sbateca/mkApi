from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.create_test_type_request_dto import TestTypeRequestDto
from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import TestTypeRequestError


class UpdateTestTypeRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    test_type_id: str = Field(alias="testTypeId")
    test_type: TestTypeRequestDto = Field(alias="testType")

    @field_validator("test_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestTypeRequestError.BLANK_TEST_TYPE_ID,
            TestTypeRequestError.INVALID_TEST_TYPE_ID,
        )
