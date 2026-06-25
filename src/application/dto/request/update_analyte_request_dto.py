from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.create_analyte_request_dto import AnalyteRequestDto
from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import AnalyteRequestError


class UpdateAnalyteRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    analyte_id: str = Field(alias="analyteId")
    analyte: AnalyteRequestDto

    @field_validator("analyte_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            AnalyteRequestError.BLANK_ANALYTE_ID,
            AnalyteRequestError.INVALID_ANALYTE_ID,
        )
