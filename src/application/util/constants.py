from enum import Enum


class ClientRequestError(Enum):
    BLANK_CLIENT_ID = "Client ID cannot be blank"
    BLANK_FIELD = "Field cannot be blank"
    INVALID_CLIENT_ID = "Client ID must be a valid UUID"


class AnalysisMethodRequestError(Enum):
    BLANK_ANALYSIS_METHOD_ID = "Analysis method ID cannot be blank"
    INVALID_ANALYSIS_METHOD_ID = "Analysis method ID must be a valid UUID"
    BLANK_NAME = "Analysis method name cannot be blank"


REQUEST_VALIDATION_FAILED_TEXT_MESSAGE = "Request validation failed"
VALID_CLIENT_ID_REGEX = r"^[A-Za-z0-9_-]+$"
