from enum import Enum


class ClientRequestError(Enum):
    BLANK_CLIENT_ID = "Client ID cannot be blank"
    BLANK_FIELD = "Field cannot be blank"
    INVALID_CLIENT_ID = "Client ID must be a valid UUID"


class AnalysisMethodRequestError(Enum):
    BLANK_ANALYSIS_METHOD_ID = "Analysis method ID cannot be blank"
    INVALID_ANALYSIS_METHOD_ID = "Analysis method ID must be a valid UUID"
    BLANK_NAME = "Analysis method name cannot be blank"


class TestTypeRequestError(Enum):
    BLANK_TEST_TYPE_ID = "Test type ID cannot be blank"
    INVALID_TEST_TYPE_ID = "Test type ID must be a valid UUID"
    BLANK_NAME = "Test type name cannot be blank"


class AnalyteRequestError(Enum):
    BLANK_ANALYTE_ID = "Analyte ID cannot be blank"
    INVALID_ANALYTE_ID = "Analyte ID must be a valid UUID"
    BLANK_TEST_TYPE_ID = "Test type ID cannot be blank"
    INVALID_TEST_TYPE_ID = "Test type ID must be a valid UUID"
    BLANK_NAME = "Analyte name cannot be blank"


class SampleTypeRequestError(Enum):
    BLANK_SAMPLE_TYPE_ID = "Sample type ID cannot be blank"
    INVALID_SAMPLE_TYPE_ID = "Sample type ID must be a valid UUID"
    BLANK_NAME = "Sample type name cannot be blank"


class CriteriaRequestError(Enum):
    BLANK_CRITERIA_ID = "Criteria ID cannot be blank"
    INVALID_CRITERIA_ID = "Criteria ID must be a valid UUID"
    BLANK_NAME = "Criteria name cannot be blank"


REQUEST_VALIDATION_FAILED_TEXT_MESSAGE = "Request validation failed"
VALID_CLIENT_ID_REGEX = r"^[A-Za-z0-9_-]+$"
