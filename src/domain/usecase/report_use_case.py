from uuid import uuid4

from domain.api.report_service_port import ReportServicePort
from domain.exception.analysis_method_exception import AnalysisMethodNotFoundError
from domain.exception.analyte_exception import AnalyteNotFoundError
from domain.exception.criteria_exception import CriteriaNotFoundError
from domain.exception.domain_exception import DomainError
from domain.exception.report_exception import (
    ReportActionDeniedError,
    ReportNotFoundError,
)
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_type_exception import TestTypeNotFoundError
from domain.model.action_decision import ActionDecision
from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.model.authorization_scope import AuthorizationScope
from domain.model.report import Report, ReportWithActions
from domain.policy.action_policy import ActionPolicy
from domain.spi.analysis_method_persistence_port import AnalysisMethodPersistencePort
from domain.spi.analyte_persistence_port import AnalytePersistencePort
from domain.spi.authorization_port import AuthorizationPort
from domain.spi.criteria_persistence_port import CriteriaPersistencePort
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.report_persistence_port import ReportPersistencePort
from domain.spi.report_test_persistence_port import ReportTestPersistencePort
from domain.spi.sample_persistence_port import SamplePersistencePort
from domain.spi.test_type_persistence_port import TestTypePersistencePort
from domain.util.constants import (
    ACTION_FORBIDDEN_ERROR_MESSAGE,
    REPORT_INVALID_STATUS_ERROR_MESSAGE,
    REPORT_LIST_FORBIDDEN_ERROR_MESSAGE,
    REPORT_NOT_APPROVED_ERROR_MESSAGE,
    REPORT_NOT_DRAFT_ERROR_MESSAGE,
    TEST_IDS_MUST_BE_UNIQUE_ERROR_MESSAGE,
    ActionDecisionCode,
    ReportStatus,
    ResourceType,
    UserRole,
)


class ReportUseCase(ReportServicePort):
    def __init__(
        self,
        report_persistence_port: ReportPersistencePort,
        sample_persistence_port: SamplePersistencePort,
        analyte_persistence_port: AnalytePersistencePort,
        analysis_method_persistence_port: AnalysisMethodPersistencePort,
        criteria_persistence_port: CriteriaPersistencePort,
        test_type_persistence_port: TestTypePersistencePort,
        report_test_persistence_port: ReportTestPersistencePort,
        authorization_port: AuthorizationPort,
        action_policy: ActionPolicy,
        logger: LoggerPort | None = None,
    ):
        self.report_persistence_port = report_persistence_port
        self.sample_persistence_port = sample_persistence_port
        self.analyte_persistence_port = analyte_persistence_port
        self.analysis_method_persistence_port = analysis_method_persistence_port
        self.criteria_persistence_port = criteria_persistence_port
        self.test_type_persistence_port = test_type_persistence_port
        self.report_test_persistence_port = report_test_persistence_port
        self.authorization_port = authorization_port
        self.action_policy = action_policy
        self.logger = logger or NullLogger()

    REPORT_ACTIONS = (
        AuthorizationAction.READ,
        AuthorizationAction.UPDATE,
        AuthorizationAction.DELETE,
        AuthorizationAction.APPROVE,
        AuthorizationAction.DOWNLOAD,
    )

    async def get_reports(self, actor: AuthenticatedUser) -> list[ReportWithActions]:
        self.logger.info("Retrieving reports")
        scope = self.authorization_port.get_scope(
            actor, AuthorizationAction.READ, ResourceType.REPORT
        )
        if scope is AuthorizationScope.ALL:
            reports = await self.report_persistence_port.get_reports()
        elif scope is AuthorizationScope.OWN and actor.client_id is not None:
            reports = await self.report_persistence_port.get_reports_by_client_id(
                actor.client_id
            )
        else:
            raise ReportActionDeniedError(
                ActionDecisionCode.FORBIDDEN.value, REPORT_LIST_FORBIDDEN_ERROR_MESSAGE
            )
        return [self._add_report_actions(report, actor) for report in reports]

    async def get_report_by_id(
        self, report_id: str, actor: AuthenticatedUser
    ) -> ReportWithActions:
        report = await self._get_report(report_id)
        self._check_action_decision(actor, AuthorizationAction.READ, report)
        return self._add_report_actions(report, actor)

    async def get_report_for_download(
        self, report_id: str, actor: AuthenticatedUser
    ) -> Report:
        report = await self._get_report(report_id)
        self._check_action_decision(actor, AuthorizationAction.DOWNLOAD, report)
        return report

    async def _get_report(self, report_id: str) -> Report:
        report = await self.report_persistence_port.get_report_by_id(report_id)
        if report is None:
            raise ReportNotFoundError()
        return report

    def get_create_decision(self, actor: AuthenticatedUser) -> ActionDecision:
        return self._get_action_decision(actor, AuthorizationAction.CREATE)

    async def create_report(self, report: Report, actor: AuthenticatedUser) -> Report:
        self._require_allowed(self.get_create_decision(actor))
        await self._validate_report_relations(report)

        report.status = ReportStatus.DRAFT.value
        report.id = report.id or uuid4()
        self.logger.info("Creating report", report_id=str(report.id))

        return await self.report_persistence_port.save_report(
            report, report_tests_port=self.report_test_persistence_port
        )

    async def update_report(
        self, report_id: str, updated_report: Report, actor: AuthenticatedUser
    ) -> Report:
        current = await self._get_report(report_id)
        self._check_action_decision(actor, AuthorizationAction.UPDATE, current)
        await self._validate_report_relations(updated_report)

        updated_report.status = current.status
        if updated_report.sample.client.id != current.sample.client.id:
            self._check_action_decision(
                actor, AuthorizationAction.UPDATE, updated_report
            )
        updated_report.id = current.id
        self.logger.info("Updating report", report_id=report_id)

        return await self.report_persistence_port.update_report(updated_report)

    async def delete_report(self, report_id: str, actor: AuthenticatedUser) -> None:
        report = await self._get_report(report_id)
        self._check_action_decision(actor, AuthorizationAction.DELETE, report)
        await self.report_persistence_port.delete_report(report_id)
        self.logger.info("Report deleted", report_id=report_id)

    async def set_report_status(
        self, report_id: str, status: str, actor: AuthenticatedUser
    ) -> Report:
        report = await self._get_report(report_id)
        self._check_action_decision(actor, AuthorizationAction.APPROVE, report)
        if status != ReportStatus.APPROVED.value:
            raise ReportActionDeniedError(
                ActionDecisionCode.INVALID_REPORT_STATUS.value,
                REPORT_INVALID_STATUS_ERROR_MESSAGE,
            )
        return await self.report_persistence_port.update_report_status(
            report_id, status
        )

    async def _validate_report_relations(self, report: Report) -> None:
        for test in report.tests:
            test.id = test.id or uuid4()
        test_ids = [test.id for test in report.tests]
        if len(test_ids) != len(set(test_ids)):
            raise DomainError(TEST_IDS_MUST_BE_UNIQUE_ERROR_MESSAGE)

        sample = await self.sample_persistence_port.get_sample_by_id(
            str(report.sample.id)
        )
        if sample is None:
            raise SampleNotFoundError()

        for test in report.tests:
            test.sample_id = str(sample.id)
            analysis_method = (
                await self.analysis_method_persistence_port.get_analysis_method_by_id(
                    test.analysis_method.id
                )
            )
            criteria = await self.criteria_persistence_port.get_criteria_by_id(
                test.criteria.id
            )
            analyte = await self.analyte_persistence_port.get_analyte_by_id(
                test.analyte.id
            )
            test_type = await self.test_type_persistence_port.get_test_type_by_id(
                test.test_type.id
            )

            if analysis_method is None:
                raise AnalysisMethodNotFoundError()
            if criteria is None:
                raise CriteriaNotFoundError()
            if analyte is None:
                raise AnalyteNotFoundError()
            if test_type is None:
                raise TestTypeNotFoundError()

            test.analysis_method = analysis_method
            test.criteria = criteria
            test.analyte = analyte
            test.test_type = test_type

        report.sample = sample

    def _check_action_decision(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        report: Report | None = None,
    ) -> None:
        self._require_allowed(self._get_action_decision(actor, action, report))

    @staticmethod
    def _require_allowed(decision: ActionDecision) -> None:
        if not decision.allowed:
            raise ReportActionDeniedError(decision.code, decision.reason)

    def _get_action_decision(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        report: Report | None = None,
    ) -> ActionDecision:
        resource = AuthorizationResource(
            ResourceType.REPORT, report.sample.client.id if report else None
        )
        if action is AuthorizationAction.DOWNLOAD and report is not None:
            return self.action_policy.evaluate_action(
                actor,
                action,
                resource,
                rule=lambda: self._check_perform_download_decision(report),
            )
        if report is not None and action in (
            AuthorizationAction.UPDATE,
            AuthorizationAction.DELETE,
            AuthorizationAction.APPROVE,
        ):
            return self.action_policy.evaluate_action(
                actor,
                action,
                resource,
                rule=lambda: self._check_perform_action_from_draft_decision(
                    actor, action, report
                ),
            )
        return self.action_policy.evaluate_action(actor, action, resource)

    @staticmethod
    def _check_perform_action_from_draft_decision(
        actor: AuthenticatedUser, action: AuthorizationAction, report: Report
    ) -> ActionDecision:
        if UserRole.CLIENT in actor.roles and action in (
            AuthorizationAction.UPDATE,
            AuthorizationAction.DELETE,
            AuthorizationAction.APPROVE,
        ):
            return ActionDecision(
                allowed=False,
                code=ActionDecisionCode.FORBIDDEN.value,
                reason=ACTION_FORBIDDEN_ERROR_MESSAGE,
            )
        if not ReportStatus.is_draft(report.status):
            return ActionDecision(
                allowed=False,
                code=ActionDecisionCode.REPORT_NOT_DRAFT.value,
                reason=REPORT_NOT_DRAFT_ERROR_MESSAGE,
            )
        return ActionDecision(allowed=True)

    @staticmethod
    def _check_perform_download_decision(report: Report) -> ActionDecision:
        if report.status in (ReportStatus.APPROVED, ReportStatus.APPROVED.value):
            return ActionDecision(allowed=True)
        return ActionDecision(
            allowed=False,
            code=ActionDecisionCode.REPORT_NOT_APPROVED.value,
            reason=REPORT_NOT_APPROVED_ERROR_MESSAGE,
        )

    def _add_report_actions(
        self, report: Report, actor: AuthenticatedUser
    ) -> ReportWithActions:
        return ReportWithActions(
            id=report.id,
            report_number=report.report_number,
            report_date=report.report_date,
            status=report.status,
            sample=report.sample,
            tests=report.tests,
            actions={
                action.value: self._get_action_decision(actor, action, report)
                for action in self.REPORT_ACTIONS
            },
        )
