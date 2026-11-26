from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    LINKED_REPORT_TEST_ERROR_MESSAGE,
    TEST_NOT_FOUND_ERROR_MESSAGE,
)


class TestNotFoundError(DomainError):
    def __init__(self):
        super().__init__(TEST_NOT_FOUND_ERROR_MESSAGE)


class LinkedReportTestError(DomainError):
    def __init__(self):
        super().__init__(LINKED_REPORT_TEST_ERROR_MESSAGE)
