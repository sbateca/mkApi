from application.dto.request import (
    AnalysisMethodRequestDto,
    GetAnalysisMethodByIdRequestDto,
)
from application.dto.response import AnalysisMethodResponseDto
from domain.model.analysis_method import AnalysisMethod


class AnalysisMethodMapper:
    def to_analysis_method(self, request: AnalysisMethodRequestDto) -> AnalysisMethod:
        return AnalysisMethod(id=None, name=request.name)

    def to_response(self, analysis_method: AnalysisMethod) -> AnalysisMethodResponseDto:
        return AnalysisMethodResponseDto(
            id=analysis_method.id,
            name=analysis_method.name,
        )

    def to_response_list(
        self, analysis_methods: list[AnalysisMethod]
    ) -> list[AnalysisMethodResponseDto]:
        return [self.to_response(method) for method in analysis_methods]

    def to_analysis_method_id(self, request: GetAnalysisMethodByIdRequestDto) -> str:
        return request.analysis_method_id
