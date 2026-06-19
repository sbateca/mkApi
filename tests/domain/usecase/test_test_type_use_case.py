from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.test_type_exception import (
    TestTypeAlreadyExistsError as DuplicateTestTypeError,
)
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from domain.model.test_type import TestType as DomainTestType
from domain.usecase.test_type_use_case import TestTypeUseCase as TypeService

TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


@pytest.mark.asyncio
async def test_create_test_type_assigns_id_and_saves():
    test_type = DomainTestType(name="Physical-Chemical")
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_name.return_value = None
    persistence_port.save_test_type.return_value = test_type
    use_case = TypeService(persistence_port)

    result = await use_case.create_test_type(test_type)

    assert result == test_type
    assert test_type.id is not None
    persistence_port.get_test_type_by_name.assert_awaited_once_with("Physical-Chemical")
    persistence_port.save_test_type.assert_awaited_once_with(test_type)


@pytest.mark.asyncio
async def test_create_test_type_rejects_duplicate_name():
    test_type = DomainTestType(name="Physical-Chemical")
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_name.return_value = DomainTestType(
        id=TEST_TYPE_ID, name=test_type.name
    )
    use_case = TypeService(persistence_port)

    with pytest.raises(DuplicateTestTypeError):
        await use_case.create_test_type(test_type)

    persistence_port.save_test_type.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_test_types_returns_persisted_items():
    test_types = [DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")]
    persistence_port = AsyncMock()
    persistence_port.get_test_types.return_value = test_types
    use_case = TypeService(persistence_port)

    assert await use_case.get_test_types() == test_types
    persistence_port.get_test_types.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_test_type_by_id_returns_existing_item():
    test_type = DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_id.return_value = test_type
    use_case = TypeService(persistence_port)

    assert await use_case.get_test_type_by_id(str(TEST_TYPE_ID)) == test_type


@pytest.mark.asyncio
async def test_get_test_type_by_id_rejects_missing_item():
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_id.return_value = None
    use_case = TypeService(persistence_port)

    with pytest.raises(MissingTestTypeError):
        await use_case.get_test_type_by_id(str(TEST_TYPE_ID))


@pytest.mark.asyncio
async def test_update_test_type_changes_name():
    current = DomainTestType(id=TEST_TYPE_ID, name="Old")
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_id.return_value = current
    persistence_port.get_test_type_by_name_excluding_id.return_value = None
    persistence_port.update_test_type.return_value = current
    use_case = TypeService(persistence_port)

    result = await use_case.update_test_type(
        str(TEST_TYPE_ID), DomainTestType(name="Physical-Chemical")
    )

    assert result.name == "Physical-Chemical"
    persistence_port.update_test_type.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_test_type_rejects_duplicate_name():
    current = DomainTestType(id=TEST_TYPE_ID, name="Old")
    duplicate = DomainTestType(name="Physical-Chemical")
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_id.return_value = current
    persistence_port.get_test_type_by_name_excluding_id.return_value = duplicate
    use_case = TypeService(persistence_port)

    with pytest.raises(DuplicateTestTypeError):
        await use_case.update_test_type(str(TEST_TYPE_ID), duplicate)

    persistence_port.update_test_type.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_test_type_deletes_existing_item():
    test_type = DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")
    persistence_port = AsyncMock()
    persistence_port.get_test_type_by_id.return_value = test_type
    use_case = TypeService(persistence_port)

    await use_case.delete_test_type(str(TEST_TYPE_ID))

    persistence_port.delete_test_type.assert_awaited_once_with(TEST_TYPE_ID)
