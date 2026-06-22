from application.dto.request import GetSampleTypeByIdRequestDto, SampleTypeRequestDto
from application.dto.response import SampleTypeResponseDto
from domain.model.sample_type import SampleType


class SampleTypeMapper:
    def to_sample_type(self, request: SampleTypeRequestDto) -> SampleType:
        return SampleType(id=None, name=request.name)

    def to_response(self, sample_type: SampleType) -> SampleTypeResponseDto:
        return SampleTypeResponseDto(id=sample_type.id, name=sample_type.name)

    def to_response_list(
        self, sample_types: list[SampleType]
    ) -> list[SampleTypeResponseDto]:
        return [self.to_response(sample_type) for sample_type in sample_types]

    def to_sample_type_id(self, request: GetSampleTypeByIdRequestDto) -> str:
        return request.sample_type_id
