from uuid import UUID

from application.util.constants import SampleTypeRequestError


def validate_sample_type_id(value: str) -> str:
    sample_type_id = value.strip()
    if not sample_type_id:
        raise ValueError(SampleTypeRequestError.BLANK_SAMPLE_TYPE_ID.value)
    try:
        UUID(sample_type_id)
    except ValueError as error:
        raise ValueError(SampleTypeRequestError.INVALID_SAMPLE_TYPE_ID.value) from error
    return sample_type_id


def validate_sample_type_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError(SampleTypeRequestError.BLANK_NAME.value)
    return name
