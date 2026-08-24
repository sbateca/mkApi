from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    ROLE_ALREADY_EXISTS_ERROR_MESSAGE,
    ROLE_NOT_FOUND_ERROR_MESSAGE,
)


class RoleNotFoundError(DomainError):
    def __init__(self):
        super().__init__(ROLE_NOT_FOUND_ERROR_MESSAGE)


class RoleAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__(ROLE_ALREADY_EXISTS_ERROR_MESSAGE)
