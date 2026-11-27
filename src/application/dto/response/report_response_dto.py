from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.response.action_response_dto import (
    ActionDecisionResponseDto,
    CollectionActionsResponseDto,
)
from application.dto.response.sample_response_dto import SampleResponseDto
from application.dto.response.test_response_dto import TestResponseDto
from domain.util.constants import ReportStatus


class ReportResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID | None
    report_number: str = Field(serialization_alias="reportNumber")
    report_date: date = Field(serialization_alias="reportDate")
    status: str
    sample: SampleResponseDto
    tests: list[TestResponseDto]

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, status: ReportStatus | str) -> str:
        return ReportStatus.normalize(status)


class ReportWithActionsResponseDto(ReportResponseDto):
    model_config = ConfigDict(populate_by_name=True)
    actions: dict[str, "ActionDecisionResponseDto"] = Field(default_factory=dict)


class ReportCollectionActionsResponseDto(CollectionActionsResponseDto):
    pass
