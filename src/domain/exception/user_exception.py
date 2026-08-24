from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    USER_ALREADY_EXISTS_ERROR_MESSAGE,
    USER_NOT_FOUND_ERROR_MESSAGE,
)


class UserNotFoundError(DomainError):
    def __init__(self):
        super().__init__(USER_NOT_FOUND_ERROR_MESSAGE)


class UserAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(USER_ALREADY_EXISTS_ERROR_MESSAGE)
