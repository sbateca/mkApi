from pydantic import BaseModel, field_validator

from application.dto.request.create_analyte_request_dto import AnalyteRequestDto
from application.dto.request.validators.analyte_validators import validate_analyte_id


class UpdateAnalyteRequestDto(BaseModel):
    analyte_id: str
    analyte: AnalyteRequestDto

    @field_validator("analyte_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_analyte_id(value)
