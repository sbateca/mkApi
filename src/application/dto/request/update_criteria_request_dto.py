from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.create_criteria_request_dto import CriteriaRequestDto
from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import CriteriaRequestError


class UpdateCriteriaRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria_id: str = Field(alias="criteriaId")
    criteria: CriteriaRequestDto

    @field_validator("criteria_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            CriteriaRequestError.BLANK_CRITERIA_ID,
            CriteriaRequestError.INVALID_CRITERIA_ID,
        )
