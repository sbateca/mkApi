from enum import Enum
from uuid import UUID


def validate_not_blank_value(value: str, blank_error: Enum) -> str:
    field = value.strip()
    if not field:
        raise ValueError(blank_error.value)
    return field


def validate_uuid(value: str, blank_error: Enum, invalid_error: Enum) -> str:
    identifier = validate_not_blank_value(value, blank_error)
    try:
        UUID(identifier)
    except ValueError as error:
        raise ValueError(invalid_error.value) from error
    return identifier
