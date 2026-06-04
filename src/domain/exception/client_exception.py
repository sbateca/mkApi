from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    CLIENT_ALREADY_EXISTS_ERROR_MESSAGE,
    CLIENT_NOT_FOUND_ERROR_MESSAGE,
)


class ClientAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(CLIENT_ALREADY_EXISTS_ERROR_MESSAGE)


class ClientNotFoundError(DomainError):
    def __init__(self):
        super().__init__(CLIENT_NOT_FOUND_ERROR_MESSAGE)
