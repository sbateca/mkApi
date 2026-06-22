from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    ANALYTE_ALREADY_EXISTS_ERROR_MESSAGE,
    ANALYTE_NOT_FOUND_ERROR_MESSAGE,
)


class AnalyteAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(ANALYTE_ALREADY_EXISTS_ERROR_MESSAGE)


class AnalyteNotFoundError(DomainError):
    def __init__(self):
        super().__init__(ANALYTE_NOT_FOUND_ERROR_MESSAGE)
