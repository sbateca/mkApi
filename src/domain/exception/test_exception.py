from domain.exception.domain_exception import DomainError
from domain.util.constants import TEST_NOT_FOUND_ERROR_MESSAGE


class TestNotFoundError(DomainError):
    def __init__(self):
        super().__init__(TEST_NOT_FOUND_ERROR_MESSAGE)
