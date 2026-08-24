from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.user_request_dto import (
    UpdateUserRequestDto,
    UserIdRequestDto,
    UserRequestDto,
)
from application.dto.response.user_response_dto import UserResponseDto
from application.handler.user_handler_interface import UserHandlerInterface
from infrastructure.configuration.dependencies import get_user_handler

router = APIRouter(prefix="/users", tags=["Users"])
Handler = Annotated[UserHandlerInterface, Depends(get_user_handler)]


def user_id_request(user_id: str) -> UserIdRequestDto:
    return UserIdRequestDto(userId=user_id)


def update_request(user_id: str, user: UserRequestDto) -> UpdateUserRequestDto:
    return UpdateUserRequestDto(userId=user_id, user=user)


@router.post("", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserRequestDto, handler: Handler) -> UserResponseDto:
    return await handler.create_user(request)


@router.get("", response_model=list[UserResponseDto])
async def get_users(handler: Handler) -> list[UserResponseDto]:
    return await handler.get_users()


@router.get("/{user_id}", response_model=UserResponseDto)
async def get_user(
    request: Annotated[UserIdRequestDto, Depends(user_id_request)], handler: Handler
) -> UserResponseDto:
    return await handler.get_user(request)


@router.put("/{user_id}", response_model=UserResponseDto)
async def update_user(
    request: Annotated[UpdateUserRequestDto, Depends(update_request)], handler: Handler
) -> UserResponseDto:
    return await handler.update_user(request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: Annotated[UserIdRequestDto, Depends(user_id_request)], handler: Handler
) -> None:
    await handler.delete_user(request)
