from uuid import uuid4

from domain.api.test_service_port import TestServicePort
from domain.exception.analysis_method_exception import AnalysisMethodNotFoundError
from domain.exception.analyte_exception import AnalyteNotFoundError
from domain.exception.criteria_exception import CriteriaNotFoundError
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_exception import TestNotFoundError
from domain.exception.test_type_exception import (
    TestTypeConsistencyError,
    TestTypeNotFoundError,
)
from domain.model.analysis_method import AnalysisMethod
from domain.model.analyte import Analyte
from domain.model.criteria import Criteria
from domain.model.sample import Sample
from domain.model.test import Test
from domain.model.test_type import TestType
from domain.spi.analysis_method_persistence_port import AnalysisMethodPersistencePort
from domain.spi.analyte_persistence_port import AnalytePersistencePort
from domain.spi.criteria_persistence_port import CriteriaPersistencePort
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.sample_persistence_port import SamplePersistencePort
from domain.spi.test_persistence_port import TestPersistencePort
from domain.spi.test_type_persistence_port import TestTypePersistencePort


class TestUseCase(TestServicePort):
    def __init__(
        self,
        test_persistence_port: TestPersistencePort,
        test_type_persistence_port: TestTypePersistencePort,
        sample_persistence_port: SamplePersistencePort,
        analyte_persistence_port: AnalytePersistencePort,
        analysis_method_persistence_port: AnalysisMethodPersistencePort,
        criteria_persistence_port: CriteriaPersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.test_persistence_port = test_persistence_port
        self.test_type_persistence_port = test_type_persistence_port
        self.sample_persistence_port = sample_persistence_port
        self.analyte_persistence_port = analyte_persistence_port
        self.analysis_method_persistence_port = analysis_method_persistence_port
        self.criteria_persistence_port = criteria_persistence_port
        self.logger = logger or NullLogger()

    async def get_tests(self) -> list[Test]:
        self.logger.info("Retrieving tests")
        tests = await self.test_persistence_port.get_tests()
        self.logger.info("Tests retrieved", count=len(tests))
        return tests

    async def get_test_by_id(self, test_id: str) -> Test:
        self.logger.info("Retrieving test", test_id=test_id)
        test = await self.__request_test_by_id(test_id)
        self.logger.info("Test retrieved", test_id=str(test.id))
        return test

    async def create_test(self, test: Test) -> Test:
        self.logger.info("Creating test", sample_id=test.sample_id)
        await self.__validate_relations(test)

        if not test.id:
            test.id = uuid4()

        created = await self.test_persistence_port.save_test(test)
        self.logger.info("Test created", test_id=str(created.id))
        return created

    async def update_test(self, test_id: str, updated_test: Test) -> Test:
        self.logger.info("Updating test", test_id=test_id)
        current_test = await self.__request_test_by_id(test_id)
        await self.__validate_relations(updated_test)

        current_test.test_type = updated_test.test_type
        current_test.sample_id = updated_test.sample_id
        current_test.analyte = updated_test.analyte
        current_test.analysis_method = updated_test.analysis_method
        current_test.criteria = updated_test.criteria
        current_test.result = updated_test.result

        updated = await self.test_persistence_port.update_test(current_test)
        self.logger.info("Test updated", test_id=str(updated.id))
        return updated

    async def delete_test(self, test_id: str) -> None:
        self.logger.info("Deleting test", test_id=test_id)
        await self.__request_test_by_id(test_id)
        await self.test_persistence_port.delete_test(test_id)
        self.logger.info("Test deleted", test_id=test_id)

    async def __validate_relations(self, test: Test) -> None:
        test.test_type = await self.__request_test_type_by_id(str(test.test_type.id))
        await self.__request_sample_by_id(test.sample_id)
        test.analyte = await self.__request_analyte_by_id(str(test.analyte.id))
        test.analysis_method = await self.__request_analysis_method_by_id(
            str(test.analysis_method.id)
        )
        test.criteria = await self.__request_criteria_by_id(str(test.criteria.id))
        await self.__validate_test_type_consistency(test)

    async def __validate_test_type_consistency(self, test: Test) -> None:
        if test.test_type.id != test.analyte.test_type.id:
            self.logger.warning(
                "Test type inconsistency between test and analyte",
                test_id=str(test.id),
                test_type_id=str(test.test_type.id),
                analyte_test_type_id=str(test.analyte.test_type.id),
            )
            raise TestTypeConsistencyError()

    async def __request_test_by_id(self, test_id: str) -> Test:
        test = await self.test_persistence_port.get_test_by_id(test_id)
        if test is None:
            self.logger.warning("Test not found", test_id=test_id)
            raise TestNotFoundError()
        return test

    async def __request_test_type_by_id(self, test_type_id: str) -> TestType:
        test_type = await self.test_type_persistence_port.get_test_type_by_id(
            test_type_id
        )
        if test_type is None:
            self.logger.warning("Test type not found", test_type_id=test_type_id)
            raise TestTypeNotFoundError()
        return test_type

    async def __request_sample_by_id(self, sample_id: str) -> Sample:
        sample = await self.sample_persistence_port.get_sample_by_id(sample_id)
        if sample is None:
            self.logger.warning("Sample not found", sample_id=sample_id)
            raise SampleNotFoundError()
        return sample

    async def __request_analyte_by_id(self, analyte_id: str) -> Analyte:
        analyte = await self.analyte_persistence_port.get_analyte_by_id(analyte_id)
        if analyte is None:
            self.logger.warning("Analyte not found", analyte_id=analyte_id)
            raise AnalyteNotFoundError()
        return analyte

    async def __request_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod:
        analysis_method = (
            await self.analysis_method_persistence_port.get_analysis_method_by_id(
                analysis_method_id
            )
        )
        if analysis_method is None:
            self.logger.warning(
                "Analysis method not found",
                analysis_method_id=analysis_method_id,
            )
            raise AnalysisMethodNotFoundError()
        return analysis_method

    async def __request_criteria_by_id(self, criteria_id: str) -> Criteria:
        criteria = await self.criteria_persistence_port.get_criteria_by_id(criteria_id)
        if criteria is None:
            self.logger.warning("Criteria not found", criteria_id=criteria_id)
            raise CriteriaNotFoundError()
        return criteria
