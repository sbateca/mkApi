from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReportRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    report_number: str = Field(alias="reportNumber", max_length=100)
    report_date: date = Field(alias="reportDate")
    status: str = Field(max_length=50)
    sample_id: UUID = Field(alias="sampleId")
    test_ids: list[UUID] = Field(alias="testIds")

    @field_validator("report_number", "status")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be blank")
        return value

    @field_validator("test_ids")
    @classmethod
    def validate_unique_tests(cls, value: list[UUID]) -> list[UUID]:
        if len(value) != len(set(value)):
            raise ValueError("Test IDs must be unique")
        return value
