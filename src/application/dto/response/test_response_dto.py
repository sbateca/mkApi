from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from application.dto.response.analysis_method_response_dto import (
    AnalysisMethodResponseDto,
)
from application.dto.response.analyte_response_dto import AnalyteResponseDto
from application.dto.response.criteria_response_dto import CriteriaResponseDto
from application.dto.response.test_type_response_dto import TestTypeResponseDto


class TestResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID | None
    test_type: TestTypeResponseDto = Field(serialization_alias="testType")
    sample_id: str = Field(serialization_alias="sampleId")
    analyte: AnalyteResponseDto
    analysis_method: AnalysisMethodResponseDto = Field(
        serialization_alias="analysisMethod"
    )
    criteria: CriteriaResponseDto
    result: str
