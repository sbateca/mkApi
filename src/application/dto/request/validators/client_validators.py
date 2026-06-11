from uuid import UUID

from application.util.constants import ClientRequestError


def validate_client_id(value: str) -> str:
    client_id = value.strip()

    if not client_id:
        raise ValueError(ClientRequestError.BLANK_CLIENT_ID.value)

    try:
        UUID(client_id)
    except ValueError as error:
        raise ValueError(ClientRequestError.INVALID_CLIENT_ID.value) from error

    return client_id


def validate_not_blank(value: str) -> str:
    if not value.strip():
        raise ValueError(ClientRequestError.BLANK_FIELD.value)

    return value.strip()
