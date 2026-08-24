from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.dto.request.validators.common_validators import validate_uuid
from application.util.constants import RoleRequestError
from domain.util.constants import UserRole


class RoleRequestDto(BaseModel):
    name: UserRole


class RoleIdRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    role_id: str = Field(alias="roleId")

    @field_validator("role_id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid(
            value,
            RoleRequestError.BLANK_ROLE_ID,
            RoleRequestError.INVALID_ROLE_ID,
        )


class UpdateRoleRequestDto(RoleIdRequestDto):
    role: RoleRequestDto
