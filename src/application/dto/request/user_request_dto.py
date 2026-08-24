from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import UserRequestError
from domain.util.constants import UserRole


class UserRequestDto(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=8, max_length=150)
    email: EmailStr
    roles: list[UserRole] = Field(min_length=1)


class UserIdRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")

    @field_validator("user_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            UserRequestError.BLANK_USER_ID,
            UserRequestError.INVALID_USER_ID,
        )


class UpdateUserRequestDto(UserIdRequestDto):
    user: UserRequestDto
