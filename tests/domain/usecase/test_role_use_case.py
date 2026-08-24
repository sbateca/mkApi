from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from domain.exception.role_exception import RoleAlreadyExistsError, RoleNotFoundError
from domain.model.role import Role
from domain.usecase.role_usecase import RoleUseCase
from domain.util.constants import UserRole

ROLE_ID = UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5")


@pytest.mark.asyncio
async def test_create_role_validates_name_and_saves():
    role = Role(name=UserRole.ANALYST)
    persistence = AsyncMock()
    persistence.find_by_name.return_value = None
    persistence.save.return_value = Role(id=ROLE_ID, name=UserRole.ANALYST)

    result = await RoleUseCase(persistence).create_role(role)

    persistence.find_by_name.assert_awaited_once_with("Analyst")
    persistence.save.assert_awaited_once_with(role)
    assert result.id == ROLE_ID


@pytest.mark.asyncio
async def test_create_role_rejects_duplicate_name():
    role = Role(name=UserRole.ANALYST)
    persistence = AsyncMock()
    persistence.find_by_name.return_value = Role(id=ROLE_ID, name=UserRole.ANALYST)

    with pytest.raises(RoleAlreadyExistsError):
        await RoleUseCase(persistence).create_role(role)

    persistence.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_role_queries_delegate_to_persistence():
    role = Role(id=ROLE_ID, name=UserRole.ADMIN)
    persistence = AsyncMock()
    persistence.find_all.return_value = [role]
    persistence.find_by_id.return_value = role
    persistence.find_by_name.return_value = role
    persistence.find_roles_by_names.return_value = [role]
    use_case = RoleUseCase(persistence)

    assert await use_case.get_roles() == [role]
    assert await use_case.get_role_by_id(str(ROLE_ID)) is role
    assert await use_case.get_role_by_name("Admin") is role
    assert await use_case.find_roles_by_names(["Admin"]) == [role]


@pytest.mark.asyncio
async def test_update_role_uses_string_name_and_preserves_id():
    current = Role(id=ROLE_ID, name=UserRole.ADMIN)
    updated = Role(name=UserRole.TECHNICAL_DIRECTOR)
    persistence = AsyncMock()
    persistence.find_by_id.return_value = current
    persistence.find_by_name.return_value = None
    persistence.update.side_effect = lambda _role_id, role: role

    result = await RoleUseCase(persistence).update_role(str(ROLE_ID), updated)

    persistence.find_by_name.assert_awaited_once_with("Technical Director")
    persistence.update.assert_awaited_once_with(str(ROLE_ID), updated)
    assert result.id == ROLE_ID


@pytest.mark.asyncio
async def test_update_role_rejects_name_owned_by_another_role():
    current = Role(id=ROLE_ID, name=UserRole.ADMIN)
    duplicate = Role(
        id=UUID("9e0f9f8c-a85d-4e4e-af88-bef8733caa90"),
        name=UserRole.ANALYST,
    )
    persistence = AsyncMock()
    persistence.find_by_id.return_value = current
    persistence.find_by_name.return_value = duplicate

    with pytest.raises(RoleAlreadyExistsError):
        await RoleUseCase(persistence).update_role(
            str(ROLE_ID), Role(name=UserRole.ANALYST)
        )

    persistence.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_role_checks_existence_then_deletes():
    persistence = AsyncMock()
    persistence.find_by_id.return_value = Role(id=ROLE_ID, name=UserRole.ADMIN)

    await RoleUseCase(persistence).delete_role(str(ROLE_ID))

    persistence.delete.assert_awaited_once_with(str(ROLE_ID))


@pytest.mark.asyncio
@pytest.mark.parametrize("operation", ["get", "update", "delete"])
async def test_role_by_id_operations_raise_when_role_is_missing(operation):
    persistence = AsyncMock()
    persistence.find_by_id.return_value = None
    use_case = RoleUseCase(persistence, Mock())

    with pytest.raises(RoleNotFoundError):
        if operation == "get":
            await use_case.get_role_by_id("missing")
        elif operation == "update":
            await use_case.update_role("missing", Role(name=UserRole.ADMIN))
        else:
            await use_case.delete_role("missing")

    persistence.update.assert_not_awaited()
    persistence.delete.assert_not_awaited()
