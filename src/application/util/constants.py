from enum import Enum


class ClientRequestError(Enum):
    BLANK_CLIENT_ID = "Client ID cannot be blank"
    BLANK_FIELD = "Field cannot be blank"
    INVALID_CLIENT_ID = "Client ID must be a valid UUID"


REQUEST_VALIDATION_FAILED_TEXT_MESSAGE = "Request validation failed"
VALID_CLIENT_ID_REGEX = r"^[A-Za-z0-9_-]+$"
