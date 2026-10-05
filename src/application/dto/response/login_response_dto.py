from pydantic import BaseModel


class LoginResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
