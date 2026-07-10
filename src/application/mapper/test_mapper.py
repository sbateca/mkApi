from uuid import UUID

from application.dto.request import GetTestByIdRequestDto, TestRequestDto
from application.dto.response import (
    AnalysisMethodResponseDto,
    AnalyteResponseDto,
    CriteriaResponseDto,
    TestResponseDto,
    TestTypeResponseDto,
)
from domain.model.analysis_method import AnalysisMethod
from domain.model.analyte import Analyte
from domain.model.criteria import Criteria
from domain.model.test import Test
from domain.model.test_type import TestType


class TestMapper:
    def to_test(self, request: TestRequestDto) -> Test:
        test_type = TestType(id=UUID(request.test_type_id), name="")
        return Test(
            id=None,
            test_type=test_type,
            sample_id=request.sample_id,
            analyte=Analyte(
                id=UUID(request.analyte_id),
                name="",
                test_type=test_type,
            ),
            analysis_method=AnalysisMethod(
                id=UUID(request.analysis_method_id),
                name="",
            ),
            criteria=Criteria(id=UUID(request.criteria_id), name=""),
            result=request.result,
        )

    def to_response(self, test: Test) -> TestResponseDto:
        return TestResponseDto(
            id=test.id,
            test_type=TestTypeResponseDto(
                id=test.test_type.id,
                name=test.test_type.name,
            ),
            sample_id=test.sample_id,
            analyte=AnalyteResponseDto(
                id=test.analyte.id,
                name=test.analyte.name,
                test_type=TestTypeResponseDto(
                    id=test.analyte.test_type.id,
                    name=test.analyte.test_type.name,
                ),
            ),
            analysis_method=AnalysisMethodResponseDto(
                id=test.analysis_method.id,
                name=test.analysis_method.name,
            ),
            criteria=CriteriaResponseDto(
                id=test.criteria.id,
                name=test.criteria.name,
            ),
            result=test.result,
        )

    def to_response_list(self, tests: list[Test]) -> list[TestResponseDto]:
        return [self.to_response(test) for test in tests]

    def to_test_id(self, request: GetTestByIdRequestDto) -> str:
        return request.test_id
