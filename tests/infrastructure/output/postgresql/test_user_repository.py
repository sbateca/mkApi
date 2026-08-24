from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.output.postgresql.entity.user_entity import UserEntity
from infrastructure.output.postgresql.entity.user_role_entity import UserRoleEntity
from infrastructure.output.postgresql.repository.user_repository import (
    UserPostgreSQLRepository,
)


@pytest.mark.asyncio
async def test_save_user_reloads_relationships_before_returning():
    user_id = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")
    user_entity = UserEntity(
        id=user_id,
        name="User prueba",
        username="admin2",
        password="hashed-password",
        email="admin2@example.com",
    )
    loaded_entity = MagicMock(spec=UserEntity)
    session = MagicMock(spec=AsyncSession)
    session.commit = AsyncMock()
    repository = UserPostgreSQLRepository(session)
    repository.get_user_by_id = AsyncMock(return_value=loaded_entity)

    result = await repository.save_user(user_entity)

    session.add.assert_called_once_with(user_entity)
    session.commit.assert_awaited_once_with()
    repository.get_user_by_id.assert_awaited_once_with(str(user_id))
    assert result is loaded_entity


@pytest.mark.asyncio
async def test_update_user_attaches_new_role_rows_to_persistent_user_only():
    user_id = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")
    role_id = UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5")
    current = UserEntity(
        id=user_id,
        name="Old name",
        username="old-username",
        password="old-hash",
        email="old@example.com",
    )
    current.user_roles = []
    updated = UserEntity(
        id=user_id,
        name="Updated name",
        username="updated-username",
        password="new-hash",
        email="updated@example.com",
    )
    source_role = UserRoleEntity(role_id=role_id)
    updated.user_roles = [source_role]
    loaded = MagicMock(spec=UserEntity)
    session = MagicMock(spec=AsyncSession)
    session.commit = AsyncMock()
    repository = UserPostgreSQLRepository(session)
    repository.get_user_by_id = AsyncMock(side_effect=[current, loaded])

    result = await repository.update_user(str(user_id), updated)

    assert current.name == "Updated name"
    assert current.username == "updated-username"
    assert current.password == "new-hash"
    assert current.email == "updated@example.com"
    assert len(current.user_roles) == 1
    assert current.user_roles[0] is not source_role
    assert current.user_roles[0].role_id == role_id
    assert current.user_roles[0].user is current
    assert source_role.user is updated
    session.commit.assert_awaited_once_with()
    assert result is loaded
