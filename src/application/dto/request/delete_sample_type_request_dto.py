from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import SampleTypeRequestError


class DeleteSampleTypeRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sample_type_id: str = Field(alias="sampleTypeId")

    @field_validator("sample_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            SampleTypeRequestError.BLANK_SAMPLE_TYPE_ID,
            SampleTypeRequestError.INVALID_SAMPLE_TYPE_ID,
        )
