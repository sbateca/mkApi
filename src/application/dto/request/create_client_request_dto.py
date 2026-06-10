from pydantic import BaseModel, EmailStr, Field, field_validator

from application.util.constants import ClientRequestError


class CreateClientRequestDto(BaseModel):
    name: str = Field(max_length=150)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    nit: str = Field(min_length=5, max_length=50)
    address: str = Field(min_length=5, max_length=250)

    @field_validator("name", "phone", "nit", "address")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(ClientRequestError.BLANK_FIELD.value)

        return value.strip()
