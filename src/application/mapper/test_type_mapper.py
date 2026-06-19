from application.dto.request import GetTestTypeByIdRequestDto, TestTypeRequestDto
from application.dto.response import TestTypeResponseDto
from domain.model.test_type import TestType


class TestTypeMapper:
    def to_test_type(self, request: TestTypeRequestDto) -> TestType:
        return TestType(id=None, name=request.name)

    def to_response(self, test_type: TestType) -> TestTypeResponseDto:
        return TestTypeResponseDto(id=test_type.id, name=test_type.name)

    def to_response_list(self, test_types: list[TestType]) -> list[TestTypeResponseDto]:
        return [self.to_response(test_type) for test_type in test_types]

    def to_test_type_id(self, request: GetTestTypeByIdRequestDto) -> str:
        return request.test_type_id
