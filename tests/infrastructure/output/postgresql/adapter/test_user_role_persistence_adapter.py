from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.role_exception import RoleNotFoundError
from domain.model.role import Role
from domain.model.user import User
from domain.util.constants import UserRole
from infrastructure.output.postgresql.adapter.role_persistence_adapter import (
    RolePersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.user_persistence_adapter import (
    UserPersistenceAdapter,
)
from infrastructure.output.postgresql.entity.role_entity import RoleEntity
from infrastructure.output.postgresql.entity.user_entity import UserEntity
from infrastructure.output.postgresql.entity.user_role_entity import UserRoleEntity
from infrastructure.output.postgresql.mapper.role_entity_mapper import RoleEntityMapper
from infrastructure.output.postgresql.mapper.user_entity_mapper import UserEntityMapper

ROLE_ID = UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5")
USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


def role_entity():
    return RoleEntity(id=ROLE_ID, name="Admin")


def user_entity():
    entity = UserEntity(
        id=USER_ID,
        name="Admin user",
        username="admin",
        password="hashed-password",
        email="admin@example.com",
    )
    join = UserRoleEntity(user_id=USER_ID, role_id=ROLE_ID)
    join.role = role_entity()
    entity.user_roles = [join]
    return entity


def user_domain():
    return User(
        id=USER_ID,
        name="Admin user",
        username="admin",
        password="hashed-password",
        email="admin@example.com",
        roles=[Role(id=ROLE_ID, name=UserRole.ADMIN)],
    )


@pytest.mark.asyncio
async def test_role_adapter_delegates_crud_and_queries_with_mapping():
    repository = AsyncMock()
    entity = role_entity()
    repository.save.return_value = entity
    repository.find_by_id.return_value = entity
    repository.find_all.return_value = [entity]
    repository.update.return_value = entity
    repository.find_by_name.return_value = entity
    repository.find_roles_by_names.return_value = [entity]
    adapter = RolePersistenceAdapter(repository, RoleEntityMapper())
    role = Role(id=ROLE_ID, name=UserRole.ADMIN)

    assert await adapter.save(role) == role
    assert await adapter.find_by_id(str(ROLE_ID)) == role
    assert await adapter.find_all() == [role]
    assert await adapter.update(str(ROLE_ID), role) == role
    assert await adapter.find_by_name("Admin") == role
    assert await adapter.find_roles_by_names(["Admin"]) == [role]
    assert await adapter.delete(str(ROLE_ID)) is None
    repository.delete.assert_awaited_once_with(str(ROLE_ID))


@pytest.mark.asyncio
async def test_role_adapter_returns_none_for_missing_role():
    repository = AsyncMock()
    repository.find_by_id.return_value = None
    repository.find_by_name.return_value = None
    adapter = RolePersistenceAdapter(repository, RoleEntityMapper())

    assert await adapter.find_by_id("missing") is None
    assert await adapter.find_by_name("missing") is None


@pytest.mark.asyncio
async def test_user_adapter_delegates_crud_and_queries_with_eager_role_mapping():
    repository = AsyncMock()
    roles = AsyncMock()
    entity = user_entity()
    repository.save_user.return_value = entity
    repository.get_user_by_id.return_value = entity
    repository.get_all_users.return_value = [entity]
    repository.update_user.return_value = entity
    repository.get_user_by_email.return_value = entity
    repository.get_user_by_username.return_value = entity
    roles.find_by_name.return_value = role_entity()
    adapter = UserPersistenceAdapter(
        repository,
        UserEntityMapper(RoleEntityMapper()),
        roles,
    )
    user = user_domain()

    assert await adapter.save(user) == user_domain()
    assert await adapter.find_by_id(str(USER_ID)) == user_domain()
    assert await adapter.find_all() == [user_domain()]
    assert await adapter.update(str(USER_ID), user) == user_domain()
    assert await adapter.find_by_email(user.email) == user_domain()
    assert await adapter.find_by_username(user.username) == user_domain()
    assert await adapter.delete(str(USER_ID)) is None
    repository.delete_user.assert_awaited_once_with(str(USER_ID))
    assert roles.find_by_name.await_count == 2


@pytest.mark.asyncio
async def test_user_adapter_returns_none_for_missing_user_queries():
    repository = AsyncMock()
    repository.get_user_by_id.return_value = None
    repository.get_user_by_email.return_value = None
    repository.get_user_by_username.return_value = None
    adapter = UserPersistenceAdapter(
        repository,
        UserEntityMapper(RoleEntityMapper()),
        AsyncMock(),
    )

    assert await adapter.find_by_id("missing") is None
    assert await adapter.find_by_email("missing@example.com") is None
    assert await adapter.find_by_username("missing") is None


@pytest.mark.asyncio
async def test_user_adapter_rejects_unknown_role_before_saving():
    repository = AsyncMock()
    roles = AsyncMock()
    roles.find_by_name.return_value = None
    adapter = UserPersistenceAdapter(
        repository,
        UserEntityMapper(RoleEntityMapper()),
        roles,
    )

    with pytest.raises(RoleNotFoundError):
        await adapter.save(user_domain())

    repository.save_user.assert_not_awaited()
