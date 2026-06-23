from application.dto.request import CriteriaRequestDto, GetCriteriaByIdRequestDto
from application.dto.response import CriteriaResponseDto
from domain.model.criteria import Criteria


class CriteriaMapper:
    def to_criteria(self, request: CriteriaRequestDto) -> Criteria:
        return Criteria(id=None, name=request.name)

    def to_response(self, criteria: Criteria) -> CriteriaResponseDto:
        return CriteriaResponseDto(id=criteria.id, name=criteria.name)

    def to_response_list(self, criteria: list[Criteria]) -> list[CriteriaResponseDto]:
        return [self.to_response(item) for item in criteria]

    def to_criteria_id(self, request: GetCriteriaByIdRequestDto) -> str:
        return request.criteria_id
