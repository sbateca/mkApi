from pydantic import BaseModel, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import AnalyteRequestError


class DeleteAnalyteRequestDto(BaseModel):
    analyte_id: str

    @field_validator("analyte_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            AnalyteRequestError.BLANK_ANALYTE_ID,
            AnalyteRequestError.INVALID_ANALYTE_ID,
        )
