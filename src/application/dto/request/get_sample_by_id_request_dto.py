from pydantic import BaseModel, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import SampleRequestError


class GetSampleByIdRequestDto(BaseModel):
    sample_id: str

    @field_validator("sample_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            SampleRequestError.BLANK_SAMPLE_ID,
            SampleRequestError.INVALID_SAMPLE_ID,
        )
