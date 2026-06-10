from uuid import UUID

from pydantic import BaseModel, field_validator

from application.util.constants import ClientRequestError


class GetClientByIdRequestDto(BaseModel):
    client_id: str

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, value: str) -> str:
        client_id = value.strip()

        if not client_id:
            raise ValueError(ClientRequestError.BLANK_CLIENT_ID.value)

        try:
            UUID(client_id)
        except ValueError as error:
            raise ValueError(ClientRequestError.INVALID_CLIENT_ID.value) from error

        return client_id
