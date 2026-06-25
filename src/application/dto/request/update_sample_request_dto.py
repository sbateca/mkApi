from pydantic import BaseModel, field_validator

from application.dto.request.create_sample_request_dto import SampleRequestDto
from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import SampleRequestError


class UpdateSampleRequestDto(BaseModel):
    sample_id: str
    sample: SampleRequestDto

    @field_validator("sample_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            SampleRequestError.BLANK_SAMPLE_ID,
            SampleRequestError.INVALID_SAMPLE_ID,
        )
