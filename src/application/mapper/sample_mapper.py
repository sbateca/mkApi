from uuid import UUID

from application.dto.request import GetSampleByIdRequestDto, SampleRequestDto
from application.dto.response import (
    SampleClientResponseDto,
    SampleResponseDto,
    SampleTypeSummaryResponseDto,
)
from domain.model.client import Client
from domain.model.sample import Sample
from domain.model.sample_type import SampleType


class SampleMapper:
    def to_sample(self, request: SampleRequestDto) -> Sample:
        return Sample(
            id=None,
            sample_code=request.sample_code,
            sample_type=SampleType(id=UUID(request.sample_type_id), name=""),
            client=Client(
                id=UUID(request.client_id),
                name="",
                email="",
                phone="",
                nit="",
                address="",
            ),
            get_sample_date=request.get_sample_date,
            reception_date=request.reception_date,
            analysis_date=request.analysis_date,
            sample_location=request.sample_location,
            responsable=request.responsable,
        )

    def to_response(self, sample: Sample) -> SampleResponseDto:
        return SampleResponseDto(
            id=sample.id,
            sample_code=sample.sample_code,
            sample_type=SampleTypeSummaryResponseDto(
                id=sample.sample_type.id,
                name=sample.sample_type.name,
            ),
            client=SampleClientResponseDto(
                id=sample.client.id,
                name=sample.client.name,
            ),
            get_sample_date=sample.get_sample_date,
            reception_date=sample.reception_date,
            analysis_date=sample.analysis_date,
            sample_location=sample.sample_location,
            responsable=sample.responsable,
        )

    def to_response_list(self, samples: list[Sample]) -> list[SampleResponseDto]:
        return [self.to_response(sample) for sample in samples]

    def to_sample_id(self, request: GetSampleByIdRequestDto) -> str:
        return request.sample_id
