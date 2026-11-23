from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.login_request_dto import LoginRequestDto
from application.dto.request.refresh_token_request_dto import RefreshTokenRequestDto
from application.dto.request.user_request_dto import UserIdRequestDto
from application.dto.response.login_response_dto import LoginResponseDto
from application.dto.response.user_response_dto import UserResponseDto
from application.handler.authentication_handler_interface import (
    AuthenticationHandlerInterface,
)
from application.handler.user_handler_interface import UserHandlerInterface
from domain.model.authenticated_user import AuthenticatedUser
from infrastructure.configuration.dependencies import (
    get_authentication_handler,
    get_user_handler,
)
from infrastructure.input.rest.security.authentication import get_authenticated_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

AuthenticationHandlerDependency = Annotated[
    AuthenticationHandlerInterface,
    Depends(get_authentication_handler),
]


@router.get("/me", response_model=UserResponseDto)
async def me(
    user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    handler: Annotated[UserHandlerInterface, Depends(get_user_handler)],
) -> UserResponseDto:
    return await handler.get_user(UserIdRequestDto(user_id=str(user.id)))


@router.post(
    "/login",
    response_model=LoginResponseDto,
    status_code=status.HTTP_200_OK,
)
async def login(
    login_request_dto: LoginRequestDto,
    handler: AuthenticationHandlerDependency,
) -> LoginResponseDto:
    return await handler.login(login_request_dto)


@router.post("/refresh", response_model=LoginResponseDto)
async def refresh(
    request_dto: RefreshTokenRequestDto,
    handler: AuthenticationHandlerDependency,
) -> LoginResponseDto:
    return await handler.refresh(request_dto)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request_dto: RefreshTokenRequestDto,
    handler: AuthenticationHandlerDependency,
) -> None:
    await handler.logout(request_dto)
