from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    ANALYSIS_METHOD_ALREADY_EXISTS_ERROR_MESSAGE,
    ANALYSIS_METHOD_NOT_FOUND_ERROR_MESSAGE,
)


class AnalysisMethodAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(ANALYSIS_METHOD_ALREADY_EXISTS_ERROR_MESSAGE)


class AnalysisMethodNotFoundError(DomainError):
    def __init__(self):
        super().__init__(ANALYSIS_METHOD_NOT_FOUND_ERROR_MESSAGE)
