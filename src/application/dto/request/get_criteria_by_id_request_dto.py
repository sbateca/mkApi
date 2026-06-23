from pydantic import BaseModel, field_validator

from application.dto.request.validators.criteria_validators import validate_criteria_id


class GetCriteriaByIdRequestDto(BaseModel):
    criteria_id: str

    @field_validator("criteria_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_criteria_id(value)
