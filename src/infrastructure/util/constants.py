from enum import Enum


class ClientErrorType(Enum):
    CLIENT_ALREADY_EXISTS = "CLIENT_ALREADY_EXISTS"
    CLIENT_NOT_FOUND = "CLIENT_NOT_FOUND"


class DomainErrorType(Enum):
    DOMAIN_ERROR = "DOMAIN_ERROR"


class UnexpectedErrorType(Enum):
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"
