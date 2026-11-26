from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TestIdsRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(alias="id")
    test_type_id: UUID = Field(alias="testTypeId")
    analysis_method_id: UUID = Field(alias="analysisMethodId")
    analyte_id: UUID = Field(alias="analyteId")
    criteria_id: UUID = Field(alias="criteriaId")
    result: str = Field(max_length=200)
    sample_id: UUID = Field(alias="sampleId")


class ReportRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    report_number: str = Field(alias="reportNumber", max_length=100)
    report_date: date = Field(alias="reportDate")
    status: str = Field(max_length=50)
    sample_id: UUID = Field(alias="sampleId")
    test_ids: list[TestIdsRequestDto] = Field(alias="testIds")

    @field_validator("report_number", "status")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be blank")
        return value

    @field_validator("test_ids")
    @classmethod
    def validate_unique_tests(
        cls, value: list["TestIdsRequestDto"]
    ) -> list["TestIdsRequestDto"]:
        test_ids = [test.id for test in value]
        if len(test_ids) != len(set(test_ids)):
            raise ValueError("Test IDs must be unique")
        return value
