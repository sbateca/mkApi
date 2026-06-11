from pydantic import BaseModel, field_validator

from application.dto.request.create_client_request_dto import ClientRequestDto
from application.dto.request.validators.client_validators import (
    validate_client_id,
)


class UpdateClientRequestDto(BaseModel):
    client_id: str
    client: ClientRequestDto

    @field_validator("client_id")
    @classmethod
    def validate_client_id_field(cls, value: str) -> str:
        return validate_client_id(value)
