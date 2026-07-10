from uuid import UUID

from domain.model.test import Test
from infrastructure.output.postgresql.entity.test_entity import TestEntity
from infrastructure.output.postgresql.mapper.analysis_method_entity_mapper import (
    AnalysisMethodEntityMapper,
)
from infrastructure.output.postgresql.mapper.analyte_entity_mapper import (
    AnalyteEntityMapper,
)
from infrastructure.output.postgresql.mapper.criteria_entity_mapper import (
    CriteriaEntityMapper,
)
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper,
)


class TestEntityMapper:
    def __init__(
        self,
        test_type_entity_mapper: TestTypeEntityMapper,
        analyte_entity_mapper: AnalyteEntityMapper,
        analysis_method_entity_mapper: AnalysisMethodEntityMapper,
        criteria_entity_mapper: CriteriaEntityMapper,
    ):
        self.test_type_entity_mapper = test_type_entity_mapper
        self.analyte_entity_mapper = analyte_entity_mapper
        self.analysis_method_entity_mapper = analysis_method_entity_mapper
        self.criteria_entity_mapper = criteria_entity_mapper

    def to_entity(self, test: Test) -> TestEntity:
        return TestEntity(
            id=test.id,
            test_type_id=test.test_type.id,
            sample_id=UUID(test.sample_id),
            analyte_id=test.analyte.id,
            analysis_method_id=test.analysis_method.id,
            criteria_id=test.criteria.id,
            result=test.result,
        )

    def to_domain(self, entity: TestEntity) -> Test | None:
        if entity:
            return Test(
                id=entity.id,
                test_type=self.test_type_entity_mapper.to_domain(entity.test_type),
                sample_id=str(entity.sample_id),
                analyte=self.analyte_entity_mapper.to_domain(entity.analyte),
                analysis_method=self.analysis_method_entity_mapper.to_domain(
                    entity.analysis_method
                ),
                criteria=self.criteria_entity_mapper.to_domain(entity.criteria),
                result=entity.result,
            )
        return None

    def to_domain_list(self, entities: list[TestEntity]) -> list[Test]:
        return [self.to_domain(entity) for entity in entities]
