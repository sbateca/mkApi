from uuid import UUID

from application.util.constants import TestTypeRequestError


def validate_test_type_id(value: str) -> str:
    test_type_id = value.strip()
    if not test_type_id:
        raise ValueError(TestTypeRequestError.BLANK_TEST_TYPE_ID.value)

    try:
        UUID(test_type_id)
    except ValueError as error:
        raise ValueError(TestTypeRequestError.INVALID_TEST_TYPE_ID.value) from error

    return test_type_id


def validate_test_type_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError(TestTypeRequestError.BLANK_NAME.value)
    return name
