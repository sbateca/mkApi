from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    SAMPLE_ALREADY_EXISTS_ERROR_MESSAGE,
    SAMPLE_NOT_FOUND_ERROR_MESSAGE,
)


class SampleAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(SAMPLE_ALREADY_EXISTS_ERROR_MESSAGE)


class SampleNotFoundError(DomainError):
    def __init__(self):
        super().__init__(SAMPLE_NOT_FOUND_ERROR_MESSAGE)
