from uuid import UUID

from application.util.constants import AnalyteRequestError


def validate_analyte_id(value: str) -> str:
    return _validate_uuid(
        value,
        AnalyteRequestError.BLANK_ANALYTE_ID,
        AnalyteRequestError.INVALID_ANALYTE_ID,
    )


def validate_analyte_test_type_id(value: str) -> str:
    return _validate_uuid(
        value,
        AnalyteRequestError.BLANK_TEST_TYPE_ID,
        AnalyteRequestError.INVALID_TEST_TYPE_ID,
    )


def validate_analyte_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError(AnalyteRequestError.BLANK_NAME.value)
    return name


def _validate_uuid(value: str, blank_error, invalid_error) -> str:
    identifier = value.strip()
    if not identifier:
        raise ValueError(blank_error.value)
    try:
        UUID(identifier)
    except ValueError as error:
        raise ValueError(invalid_error.value) from error
    return identifier
