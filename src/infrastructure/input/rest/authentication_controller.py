from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.login_request_dto import LoginRequestDto
from application.dto.request.refresh_token_request_dto import RefreshTokenRequestDto
from application.dto.response.login_response_dto import LoginResponseDto
from application.handler.authentication_handler_interface import (
    AuthenticationHandlerInterface,
)
from infrastructure.configuration.dependencies import get_authentication_handler

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

AuthenticationHandlerDependency = Annotated[
    AuthenticationHandlerInterface,
    Depends(get_authentication_handler),
]


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
