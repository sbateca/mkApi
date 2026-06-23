from uuid import UUID

from application.util.constants import CriteriaRequestError


def validate_criteria_id(value: str) -> str:
    criteria_id = value.strip()
    if not criteria_id:
        raise ValueError(CriteriaRequestError.BLANK_CRITERIA_ID.value)
    try:
        UUID(criteria_id)
    except ValueError as error:
        raise ValueError(CriteriaRequestError.INVALID_CRITERIA_ID.value) from error
    return criteria_id


def validate_criteria_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError(CriteriaRequestError.BLANK_NAME.value)
    return name
