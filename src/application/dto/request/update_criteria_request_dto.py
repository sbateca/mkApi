from pydantic import BaseModel, field_validator

from application.dto.request.create_criteria_request_dto import CriteriaRequestDto
from application.dto.request.validators.criteria_validators import validate_criteria_id


class UpdateCriteriaRequestDto(BaseModel):
    criteria_id: str
    criteria: CriteriaRequestDto

    @field_validator("criteria_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_criteria_id(value)
