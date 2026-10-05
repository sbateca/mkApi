from domain.exception.domain_exception import DomainError
from domain.util.constants import AUTHENTICATION_FAILED_ERROR_MESSAGE


class AuthenticationError(DomainError):
    def __init__(self):
        super().__init__(AUTHENTICATION_FAILED_ERROR_MESSAGE)
