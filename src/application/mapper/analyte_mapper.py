from uuid import UUID

from application.dto.request import AnalyteRequestDto, GetAnalyteByIdRequestDto
from application.dto.response import AnalyteResponseDto, TestTypeResponseDto
from domain.model.analyte import Analyte
from domain.model.test_type import TestType


class AnalyteMapper:
    def to_analyte(self, request: AnalyteRequestDto) -> Analyte:
        return Analyte(
            id=None,
            name=request.name,
            test_type=TestType(id=UUID(request.test_type_id), name=""),
        )

    def to_response(self, analyte: Analyte) -> AnalyteResponseDto:
        return AnalyteResponseDto(
            id=analyte.id,
            name=analyte.name,
            test_type=TestTypeResponseDto(
                id=analyte.test_type.id,
                name=analyte.test_type.name,
            ),
        )

    def to_response_list(self, analytes: list[Analyte]) -> list[AnalyteResponseDto]:
        return [self.to_response(analyte) for analyte in analytes]

    def to_analyte_id(self, request: GetAnalyteByIdRequestDto) -> str:
        return request.analyte_id
