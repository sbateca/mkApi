from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    TEST_TYPE_ALREADY_EXISTS_ERROR_MESSAGE,
    TEST_TYPE_CONSISTENCY_ERROR_MESSAGE,
    TEST_TYPE_NOT_FOUND_ERROR_MESSAGE,
)


class TestTypeAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(TEST_TYPE_ALREADY_EXISTS_ERROR_MESSAGE)


class TestTypeNotFoundError(DomainError):
    def __init__(self):
        super().__init__(TEST_TYPE_NOT_FOUND_ERROR_MESSAGE)


class TestTypeConsistencyError(DomainError):
    __test__ = False

    def __init__(self):
        super().__init__(TEST_TYPE_CONSISTENCY_ERROR_MESSAGE)
