from uuid import UUID, uuid4

from domain.api.report_service_port import ReportServicePort
from domain.exception.domain_exception import DomainError
from domain.exception.report_exception import (
    ReportNotFoundError,
    ReportSampleConsistencyError,
)
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_exception import TestNotFoundError
from domain.model.report import Report
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.report_persistence_port import ReportPersistencePort
from domain.spi.sample_persistence_port import SamplePersistencePort
from domain.spi.test_persistence_port import TestPersistencePort
from domain.util.constants import TEST_IDS_MUST_BE_UNIQUE_ERROR_MESSAGE


class ReportUseCase(ReportServicePort):
    def __init__(
        self,
        report_persistence_port: ReportPersistencePort,
        sample_persistence_port: SamplePersistencePort,
        test_persistence_port: TestPersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.report_persistence_port = report_persistence_port
        self.sample_persistence_port = sample_persistence_port
        self.test_persistence_port = test_persistence_port
        self.logger = logger or NullLogger()

    async def get_reports(self) -> list[Report]:
        self.logger.info("Retrieving reports")
        return await self.report_persistence_port.get_reports()

    async def get_report_by_id(self, report_id: str) -> Report:
        report = await self.report_persistence_port.get_report_by_id(report_id)
        if report is None:
            raise ReportNotFoundError()
        return report

    async def create_report(self, report: Report) -> Report:
        await self._validate_report_relations(report)
        report.id = report.id or uuid4()
        self.logger.info("Creating report", report_id=str(report.id))
        return await self.report_persistence_port.save_report(report)

    async def update_report(self, report_id: str, updated_report: Report) -> Report:
        current = await self.get_report_by_id(report_id)
        await self._validate_report_relations(updated_report)
        updated_report.id = current.id
        self.logger.info("Updating report", report_id=report_id)
        return await self.report_persistence_port.update_report(updated_report)

    async def delete_report(self, report_id: str) -> None:
        await self.get_report_by_id(report_id)
        await self.report_persistence_port.delete_report(report_id)
        self.logger.info("Report deleted", report_id=report_id)

    async def set_report_status(self, report_id: str, status: str) -> Report:
        report = await self.get_report_by_id(report_id)
        report.status = status
        return await self.report_persistence_port.update_report(report)

    async def _validate_report_relations(self, report: Report) -> None:
        sample = await self.sample_persistence_port.get_sample_by_id(
            str(report.sample.id)
        )

        if sample is None:
            raise SampleNotFoundError()
        test_ids = [test.id for test in report.tests]

        if len(test_ids) != len(set(test_ids)):
            raise DomainError(TEST_IDS_MUST_BE_UNIQUE_ERROR_MESSAGE)
        tests = []

        for test_id in test_ids:
            test = await self.test_persistence_port.get_test_by_id(str(test_id))
            if test is None:
                raise TestNotFoundError()
            if UUID(test.sample_id) != sample.id:
                raise ReportSampleConsistencyError()
            tests.append(test)

        report.sample = sample
        report.tests = tests
