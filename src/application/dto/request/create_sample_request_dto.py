from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import (
    validate_not_blank_value,
    validate_uuid,
)
from application.util.constants import SampleRequestError
from domain.util.str_functions import capitalize_str


class SampleRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sample_code: str = Field(alias="sampleCode", max_length=50)
    sample_type_id: str = Field(alias="sampleTypeId")
    client_id: str = Field(alias="clientId")
    get_sample_date: date = Field(alias="getSampleDate")
    reception_date: date = Field(alias="receptionDate")
    analysis_date: date = Field(alias="analysisDate")
    sample_location: str = Field(alias="sampleLocation", max_length=250)
    responsable: str = Field(max_length=150)

    @field_validator("sample_code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        return validate_not_blank_value(value, SampleRequestError.BLANK_SAMPLE_CODE)

    @field_validator("sample_type_id")
    @classmethod
    def validate_type_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            SampleRequestError.BLANK_SAMPLE_TYPE_ID,
            SampleRequestError.INVALID_SAMPLE_TYPE_ID,
        )

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            SampleRequestError.BLANK_CLIENT_ID,
            SampleRequestError.INVALID_CLIENT_ID,
        )

    @field_validator("sample_location", "responsable")
    @classmethod
    def validate_text_field(cls, value: str) -> str:
        capitalized_value = capitalize_str(value)
        return validate_not_blank_value(
            capitalized_value,
            SampleRequestError.BLANK_FIELD,
        )
