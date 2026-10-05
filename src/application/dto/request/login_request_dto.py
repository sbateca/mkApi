from pydantic import BaseModel, Field, field_validator

from application.util.constants import LoginRequestError


class LoginRequestDto(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1, max_length=150)

    @field_validator("username")
    @classmethod
    def username_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(LoginRequestError.BLANK_USERNAME.value)
        return value
