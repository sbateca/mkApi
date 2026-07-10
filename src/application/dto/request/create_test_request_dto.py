from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import (
    validate_not_blank_value,
    validate_uuid,
)
from application.util.constants import TestRequestError


class TestRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    test_type_id: str = Field(alias="testTypeId")
    sample_id: str = Field(alias="sampleId")
    analyte_id: str = Field(alias="analyteId")
    analysis_method_id: str = Field(alias="analysisMethodId")
    criteria_id: str = Field(alias="criteriaId")
    result: str = Field(max_length=150)

    @field_validator("test_type_id")
    @classmethod
    def validate_test_type_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestRequestError.BLANK_TEST_TYPE_ID,
            TestRequestError.INVALID_TEST_TYPE_ID,
        )

    @field_validator("sample_id")
    @classmethod
    def validate_sample_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestRequestError.BLANK_SAMPLE_ID,
            TestRequestError.INVALID_SAMPLE_ID,
        )

    @field_validator("analyte_id")
    @classmethod
    def validate_analyte_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestRequestError.BLANK_ANALYTE_ID,
            TestRequestError.INVALID_ANALYTE_ID,
        )

    @field_validator("analysis_method_id")
    @classmethod
    def validate_analysis_method_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestRequestError.BLANK_ANALYSIS_METHOD_ID,
            TestRequestError.INVALID_ANALYSIS_METHOD_ID,
        )

    @field_validator("criteria_id")
    @classmethod
    def validate_criteria_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            TestRequestError.BLANK_CRITERIA_ID,
            TestRequestError.INVALID_CRITERIA_ID,
        )

    @field_validator("result")
    @classmethod
    def validate_result(cls, value: str) -> str:
        return validate_not_blank_value(value, TestRequestError.BLANK_RESULT)
