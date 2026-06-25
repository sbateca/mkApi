from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import ClientRequestError


class GetClientByIdRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_id: str = Field(alias="clientId")

    @field_validator("client_id")
    @classmethod
    def validate_client_id_request(cls, value: str) -> str:
        return validate_uuid(
            value,
            ClientRequestError.BLANK_CLIENT_ID,
            ClientRequestError.INVALID_CLIENT_ID,
        )
