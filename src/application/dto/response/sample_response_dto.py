from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SampleClientResponseDto(BaseModel):
    id: UUID | None
    name: str


class SampleTypeSummaryResponseDto(BaseModel):
    id: UUID | None
    name: str


class SampleResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID | None
    sample_code: str = Field(serialization_alias="sampleCode")
    sample_type: SampleTypeSummaryResponseDto = Field(serialization_alias="sampleType")
    client: SampleClientResponseDto
    get_sample_date: date = Field(serialization_alias="getSampleDate")
    reception_date: date = Field(serialization_alias="receptionDate")
    analysis_date: date = Field(serialization_alias="analysisDate")
    sample_location: str = Field(serialization_alias="sampleLocation")
    responsable: str
