from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    SAMPLE_TYPE_ALREADY_EXISTS_ERROR_MESSAGE,
    SAMPLE_TYPE_NOT_FOUND_ERROR_MESSAGE,
)


class SampleTypeAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(SAMPLE_TYPE_ALREADY_EXISTS_ERROR_MESSAGE)


class SampleTypeNotFoundError(DomainError):
    def __init__(self):
        super().__init__(SAMPLE_TYPE_NOT_FOUND_ERROR_MESSAGE)
