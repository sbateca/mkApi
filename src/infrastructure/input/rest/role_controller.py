from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.role_request_dto import (
    RoleIdRequestDto,
    RoleRequestDto,
    UpdateRoleRequestDto,
)
from application.dto.response.role_response_dto import RoleResponseDto
from application.handler.role_handler_interface import RoleHandlerInterface
from domain.model.authorization_action import AuthorizationAction
from domain.util.constants import ResourceType
from infrastructure.configuration.dependencies import get_role_handler
from infrastructure.input.rest.security.authorization import require_permission

router = APIRouter(prefix="/roles", tags=["Roles"])
Handler = Annotated[RoleHandlerInterface, Depends(get_role_handler)]


def role_id_request(role_id: str) -> RoleIdRequestDto:
    return RoleIdRequestDto(roleId=role_id)


def update_request(role_id: str, role: RoleRequestDto) -> UpdateRoleRequestDto:
    return UpdateRoleRequestDto(roleId=role_id, role=role)


@router.post(
    "",
    response_model=RoleResponseDto,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(AuthorizationAction.CREATE, ResourceType.ROLE))
    ],
)
async def create_role(request: RoleRequestDto, handler: Handler) -> RoleResponseDto:
    return await handler.create_role(request)


@router.get(
    "",
    response_model=list[RoleResponseDto],
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.ROLE))
    ],
)
async def get_roles(handler: Handler) -> list[RoleResponseDto]:
    return await handler.get_roles()


@router.get(
    "/{role_id}",
    response_model=RoleResponseDto,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.ROLE))
    ],
)
async def get_role(
    request: Annotated[RoleIdRequestDto, Depends(role_id_request)], handler: Handler
) -> RoleResponseDto:
    return await handler.get_role(request)


@router.put(
    "/{role_id}",
    response_model=RoleResponseDto,
    dependencies=[
        Depends(require_permission(AuthorizationAction.UPDATE, ResourceType.ROLE))
    ],
)
async def update_role(
    request: Annotated[UpdateRoleRequestDto, Depends(update_request)], handler: Handler
) -> RoleResponseDto:
    return await handler.update_role(request)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission(AuthorizationAction.DELETE, ResourceType.ROLE))
    ],
)
async def delete_role(
    request: Annotated[RoleIdRequestDto, Depends(role_id_request)], handler: Handler
) -> None:
    await handler.delete_role(request)
