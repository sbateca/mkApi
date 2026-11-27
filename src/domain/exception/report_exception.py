from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    REPORT_ACTION_DENIED_ERROR_MESSAGE,
    REPORT_ALREADY_EXISTS_ERROR_MESSAGE,
    REPORT_NOT_FOUND_ERROR_MESSAGE,
    REPORT_SAMPLE_CONSISTENCY_ERROR_MESSAGE,
)


class ReportAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(REPORT_ALREADY_EXISTS_ERROR_MESSAGE)


class ReportNotFoundError(DomainError):
    def __init__(self):
        super().__init__(REPORT_NOT_FOUND_ERROR_MESSAGE)


class ReportSampleConsistencyError(DomainError):
    def __init__(self):
        super().__init__(REPORT_SAMPLE_CONSISTENCY_ERROR_MESSAGE)


class ReportActionDeniedError(DomainError):
    def __init__(self, code: str, reason: str):
        super().__init__(
            REPORT_ACTION_DENIED_ERROR_MESSAGE.format(code=code, reason=reason)
        )
