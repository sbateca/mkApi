from pydantic import BaseModel, field_validator

from application.dto.request.validators.client_validators import validate_client_id


class DeleteClientRequestDto(BaseModel):
    client_id: str

    @field_validator("client_id")
    @classmethod
    def validate_client_id_request(cls, value: str) -> str:
        return validate_client_id(value)
