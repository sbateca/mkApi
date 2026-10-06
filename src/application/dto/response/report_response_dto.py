from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from application.dto.response.sample_response_dto import SampleResponseDto
from application.dto.response.test_response_dto import TestResponseDto


class ReportResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID | None
    report_number: str = Field(serialization_alias="reportNumber")
    report_date: date = Field(serialization_alias="reportDate")
    status: str
    sample: SampleResponseDto
    tests: list[TestResponseDto]
