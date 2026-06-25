from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import AnalysisMethodRequestError


class GetAnalysisMethodByIdRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    analysis_method_id: str = Field(alias="analysisMethodId")

    @field_validator("analysis_method_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            AnalysisMethodRequestError.BLANK_ANALYSIS_METHOD_ID,
            AnalysisMethodRequestError.INVALID_ANALYSIS_METHOD_ID,
        )
