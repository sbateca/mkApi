from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from domain.exception.user_exception import UserAlreadyExistsError, UserNotFoundError
from domain.model.role import Role
from domain.model.user import User
from domain.usecase.user_use_case import UserUseCase
from domain.util.constants import UserRole


def make_user(*, user_id=None, email="admin2@example.com", username="admin2"):
    return User(
        id=user_id,
        name="User prueba",
        username=username,
        password="plain-password",
        email=email,
        roles=[Role(name=UserRole.ADMIN)],
    )


def make_use_case(user_persistence=None, role_persistence=None, password_hasher=None):
    return UserUseCase(
        user_persistence or AsyncMock(),
        role_persistence or AsyncMock(),
        password_hasher or Mock(),
    )


@pytest.mark.asyncio
async def test_create_user_validates_resolves_hashes_assigns_id_and_saves():
    user = make_user()
    resolved_roles = [Role(name=UserRole.ADMIN)]
    persistence = AsyncMock()
    persistence.find_by_email.return_value = None
    persistence.find_by_username.return_value = None
    persistence.save.side_effect = lambda saved_user: saved_user
    roles = AsyncMock()
    roles.find_roles_by_names.return_value = resolved_roles
    hasher = Mock()
    hasher.hash.return_value = "hashed-password"

    result = await make_use_case(persistence, roles, hasher).create_user(user)

    assert result.id is not None
    assert result.password == "hashed-password"
    assert result.roles == resolved_roles
    roles.find_roles_by_names.assert_awaited_once_with(["Admin"])
    persistence.save.assert_awaited_once_with(user)


@pytest.mark.asyncio
@pytest.mark.parametrize("duplicate_field", ["email", "username"])
async def test_create_user_rejects_duplicate_email_or_username(duplicate_field):
    user = make_user()
    persistence = AsyncMock()
    persistence.find_by_email.return_value = (
        make_user(user_id=UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e"))
        if duplicate_field == "email"
        else None
    )
    persistence.find_by_username.return_value = (
        make_user(user_id=UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e"))
        if duplicate_field == "username"
        else None
    )

    with pytest.raises(UserAlreadyExistsError):
        await make_use_case(persistence).create_user(user)

    persistence.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_user_queries_and_delete_delegate_to_persistence():
    user_id = "a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e"
    user = make_user(user_id=UUID(user_id))
    persistence = AsyncMock()
    persistence.find_all.return_value = [user]
    persistence.find_by_id.return_value = user
    persistence.find_by_email.return_value = user
    use_case = make_use_case(persistence)

    assert await use_case.get_users() == [user]
    assert await use_case.get_user_by_id(user_id) is user
    assert await use_case.get_user_by_email(user.email) is user
    assert await use_case.delete_user(user_id) is None
    persistence.delete.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("operation", ["get", "delete"])
async def test_user_by_id_operations_raise_when_user_is_missing(operation):
    persistence = AsyncMock()
    persistence.find_by_id.return_value = None
    use_case = make_use_case(persistence)

    with pytest.raises(UserNotFoundError):
        if operation == "get":
            await use_case.get_user_by_id("missing")
        else:
            await use_case.delete_user("missing")

    persistence.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_user_queries_roles_by_string_value_and_awaits_uniqueness_checks():
    user_id = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")
    current_user = User(
        id=user_id,
        name="User prueba",
        username="admin2",
        password="old-hash",
        email="admin2@example.com",
        roles=[Role(name=UserRole.ADMIN)],
    )
    updated_user = User(
        name="Updated user",
        username="admin2",
        password="new-password",
        email="admin2@example.com",
        roles=[Role(name=UserRole.TECHNICAL_DIRECTOR)],
    )
    resolved_roles = [
        Role(
            id=UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5"),
            name=UserRole.TECHNICAL_DIRECTOR,
        )
    ]
    user_persistence = AsyncMock()
    user_persistence.find_by_id.return_value = current_user
    user_persistence.find_by_email.return_value = current_user
    user_persistence.find_by_username.return_value = current_user
    user_persistence.update.return_value = updated_user
    role_persistence = AsyncMock()
    role_persistence.find_roles_by_names.return_value = resolved_roles
    password_hasher = Mock()
    password_hasher.hash.return_value = "new-hash"
    use_case = UserUseCase(user_persistence, role_persistence, password_hasher)

    result = await use_case.update_user(str(user_id), updated_user)

    user_persistence.find_by_email.assert_awaited_once_with("admin2@example.com")
    user_persistence.find_by_username.assert_awaited_once_with("admin2")
    role_persistence.find_roles_by_names.assert_awaited_once_with(
        ["Technical Director"]
    )
    user_persistence.update.assert_awaited_once_with(str(user_id), updated_user)
    assert updated_user.id == user_id
    assert updated_user.password == "new-hash"
    assert updated_user.roles == resolved_roles
    assert result is updated_user
