from enum import Enum

DOMAIN_ERROR_MESSAGE = "A domain error occurred"
UNEXPECTED_ERROR_MESSAGE = "An unexpected error occurred"

CLIENT_ALREADY_EXISTS_ERROR_MESSAGE = "The client already exists."
CLIENT_NOT_FOUND_ERROR_MESSAGE = "The client was not found."

ANALYSIS_METHOD_ALREADY_EXISTS_ERROR_MESSAGE = "The analysis method already exists."
ANALYSIS_METHOD_NOT_FOUND_ERROR_MESSAGE = "The analysis method was not found."

TEST_TYPE_ALREADY_EXISTS_ERROR_MESSAGE = "The test type already exists."
TEST_TYPE_NOT_FOUND_ERROR_MESSAGE = "The test type was not found."
TEST_TYPE_CONSISTENCY_ERROR_MESSAGE = (
    "Test type inconsistency between test and analyte."
)

ANALYTE_ALREADY_EXISTS_ERROR_MESSAGE = "The analyte already exists."
ANALYTE_NOT_FOUND_ERROR_MESSAGE = "The analyte was not found."

SAMPLE_TYPE_ALREADY_EXISTS_ERROR_MESSAGE = "The sample type already exists."
SAMPLE_TYPE_NOT_FOUND_ERROR_MESSAGE = "The sample type was not found."

CRITERIA_ALREADY_EXISTS_ERROR_MESSAGE = "The criteria already exists."
CRITERIA_NOT_FOUND_ERROR_MESSAGE = "The criteria was not found."

SAMPLE_ALREADY_EXISTS_ERROR_MESSAGE = "The sample already exists."
SAMPLE_NOT_FOUND_ERROR_MESSAGE = "The sample was not found."
SAMPLE_CLIENT_CHANGE_WITH_APPROVED_REPORT_ERROR_MESSAGE = (
    "The client cannot be changed when the sample has an approved report."
)

TEST_NOT_FOUND_ERROR_MESSAGE = "The test was not found."
LINKED_REPORT_TEST_ERROR_MESSAGE = (
    "A test linked to a report can only be changed through that report."
)
TEST_IDS_MUST_BE_UNIQUE_ERROR_MESSAGE = "Test IDs must be unique."

ROLE_NOT_FOUND_ERROR_MESSAGE = "The role was not found."
ROLE_ALREADY_EXISTS_ERROR_MESSAGE = "The role already exists."
USER_NOT_FOUND_ERROR_MESSAGE = "The user was not found."
USER_ALREADY_EXISTS_ERROR_MESSAGE = "The user already exists."
USER_CLIENT_REQUIRED_ERROR_MESSAGE = "A user with the Client role requires a client."
AUTHENTICATION_FAILED_ERROR_MESSAGE = (
    "Authentication failed. Invalid username or password."
)


ACTION_FORBIDDEN_ERROR_MESSAGE = "Doesn't have permission to perform this action"
REPORT_NOT_FOUND_ERROR_MESSAGE = "The report was not found."
REPORT_TEST_ID_ALREADY_EXISTS_ERROR_MESSAGE = "A new report test ID already exists."
REPORT_SAMPLE_CONSISTENCY_ERROR_MESSAGE = (
    "Every report test must belong to the report sample."
)
REPORT_ACTION_DENIED_ERROR_MESSAGE = "The report action was denied: {code} - {reason}"
REPORT_LIST_FORBIDDEN_ERROR_MESSAGE = "Cannot list reports"
REPORT_INVALID_STATUS_ERROR_MESSAGE = "Expected Approved"
REPORT_NOT_APPROVED_ERROR_MESSAGE = "Only approved reports can be downloaded"
REPORT_NOT_DRAFT_ERROR_MESSAGE = "Only draft reports can be edited, deleted or approved"


class ActionDecisionCode(Enum):
    FORBIDDEN = "forbidden"
    INVALID_REPORT_STATUS = "invalid_report_status"
    REPORT_NOT_APPROVED = "report_not_approved"
    REPORT_NOT_DRAFT = "report_not_draft"


class UserRole(Enum):
    ADMIN = "Admin"
    TECHNICAL_DIRECTOR = "Technical Director"
    ANALYST = "Analyst"
    RECEPTIONIST = "Receptionist"
    CLIENT = "Client"


class ReportStatus(Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    ISSUED = "Issued"

    @classmethod
    def is_draft(cls, status: "ReportStatus | str") -> bool:
        return status is cls.DRAFT or (
            isinstance(status, str) and status.lower() == cls.DRAFT.value.lower()
        )


class ResourceType(Enum):
    CLIENT = "client"
    ANALYSIS_METHOD = "analysis_method"
    TEST_TYPE = "test_type"
    ANALYTE = "analyte"
    SAMPLE_TYPE = "sample_type"
    CRITERIA = "criteria"
    SAMPLE = "sample"
    TEST = "test"
    ROLE = "role"
    USER = "user"
    REPORT = "report"
