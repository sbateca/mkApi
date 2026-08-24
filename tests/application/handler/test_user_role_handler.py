from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request.role_request_dto import (
    RoleIdRequestDto,
    RoleRequestDto,
    UpdateRoleRequestDto,
)
from application.dto.request.user_request_dto import (
    UpdateUserRequestDto,
    UserIdRequestDto,
    UserRequestDto,
)
from application.handler.impl.role_handler import RoleHandler
from application.handler.impl.user_handler import UserHandler
from application.mapper.role_mapper import RoleMapper
from application.mapper.user_mapper import UserMapper
from domain.model.role import Role
from domain.model.user import User
from domain.util.constants import UserRole

ROLE_ID = UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5")
USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


@pytest.mark.asyncio
async def test_role_handler_maps_and_delegates_all_operations():
    role = Role(id=ROLE_ID, name=UserRole.ADMIN)
    service = AsyncMock()
    service.create_role.return_value = role
    service.get_roles.return_value = [role]
    service.get_role_by_id.return_value = role
    service.update_role.return_value = role
    handler = RoleHandler(RoleMapper(), service)
    request = RoleRequestDto(name=UserRole.ADMIN)
    id_request = RoleIdRequestDto(roleId=str(ROLE_ID))

    assert (await handler.create_role(request)).id == ROLE_ID
    assert (await handler.get_roles())[0].id == ROLE_ID
    assert (await handler.get_role(id_request)).id == ROLE_ID
    assert (
        await handler.update_role(
            UpdateRoleRequestDto(roleId=str(ROLE_ID), role=request)
        )
    ).id == ROLE_ID
    assert await handler.delete_role(id_request) is None
    service.get_role_by_id.assert_awaited_once_with(str(ROLE_ID))
    service.delete_role.assert_awaited_once_with(str(ROLE_ID))


@pytest.mark.asyncio
async def test_user_handler_maps_and_delegates_all_operations():
    role = Role(id=ROLE_ID, name=UserRole.ADMIN)
    user = User(
        id=USER_ID,
        name="Admin user",
        username="admin",
        password="hashed-password",
        email="admin@example.com",
        roles=[role],
    )
    service = AsyncMock()
    service.create_user.return_value = user
    service.get_users.return_value = [user]
    service.get_user_by_id.return_value = user
    service.update_user.return_value = user
    handler = UserHandler(UserMapper(), service)
    request = UserRequestDto(
        name=user.name,
        username=user.username,
        password="password-123",
        email=user.email,
        roles=[UserRole.ADMIN],
    )
    id_request = UserIdRequestDto(userId=str(USER_ID))

    assert (await handler.create_user(request)).id == USER_ID
    assert (await handler.get_users())[0].id == USER_ID
    assert (await handler.get_user(id_request)).id == USER_ID
    assert (
        await handler.update_user(
            UpdateUserRequestDto(userId=str(USER_ID), user=request)
        )
    ).id == USER_ID
    assert await handler.delete_user(id_request) is None
    service.get_user_by_id.assert_awaited_once_with(str(USER_ID))
    service.delete_user.assert_awaited_once_with(str(USER_ID))
