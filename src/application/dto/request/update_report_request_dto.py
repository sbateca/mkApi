from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.create_report_request_dto import ReportRequestDto
from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import ReportRequestError


class UpdateReportRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    report_id: str = Field(alias="reportId")
    report: ReportRequestDto

    @field_validator("report_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            ReportRequestError.BLANK_REPORT_ID,
            ReportRequestError.INVALID_REPORT_ID,
        )
