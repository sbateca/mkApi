from pydantic import BaseModel, EmailStr, Field, field_validator

from application.dto.request.validators.common_validators import (
    validate_not_blank_value,
)
from application.util.constants import ClientRequestError
from domain.util.str_functions import capitalize_str


class ClientRequestDto(BaseModel):
    name: str = Field(max_length=150)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    nit: str = Field(min_length=5, max_length=50)
    address: str = Field(min_length=5, max_length=250)

    @field_validator("phone", "nit", "address")
    @classmethod
    def validate_not_blank_field(cls, value: str) -> str:
        return validate_not_blank_value(value, ClientRequestError.BLANK_FIELD)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        value = validate_not_blank_value(value, ClientRequestError.BLANK_FIELD)
        return capitalize_str(value)
