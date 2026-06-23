from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    CRITERIA_ALREADY_EXISTS_ERROR_MESSAGE,
    CRITERIA_NOT_FOUND_ERROR_MESSAGE,
)


class CriteriaAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(CRITERIA_ALREADY_EXISTS_ERROR_MESSAGE)


class CriteriaNotFoundError(DomainError):
    def __init__(self):
        super().__init__(CRITERIA_NOT_FOUND_ERROR_MESSAGE)
