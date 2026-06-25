from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.create_sample_type_request_dto import (
    SampleTypeRequestDto,
)
from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import SampleTypeRequestError


class UpdateSampleTypeRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sample_type_id: str = Field(alias="sampleTypeId")
    sample_type: SampleTypeRequestDto = Field(alias="sampleType")

    @field_validator("sample_type_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            SampleTypeRequestError.BLANK_SAMPLE_TYPE_ID,
            SampleTypeRequestError.INVALID_SAMPLE_TYPE_ID,
        )
