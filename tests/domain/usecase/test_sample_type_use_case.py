from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.sample_type_exception import (
    SampleTypeAlreadyExistsError as DuplicateSampleTypeError,
)
from domain.exception.sample_type_exception import (
    SampleTypeNotFoundError as MissingSampleTypeError,
)
from domain.model.sample_type import SampleType as DomainSampleType
from domain.usecase.sample_type_use_case import SampleTypeUseCase as TypeService

SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")


@pytest.mark.asyncio
async def test_create_sample_type_assigns_id_and_saves():
    sample_type = DomainSampleType(name="Bottled water")
    port = AsyncMock()
    port.get_sample_type_by_name.return_value = None
    port.save_sample_type.return_value = sample_type
    service = TypeService(port)

    assert await service.create_sample_type(sample_type) == sample_type
    assert sample_type.id is not None
    port.get_sample_type_by_name.assert_awaited_once_with("Bottled water")
    port.save_sample_type.assert_awaited_once_with(sample_type)


@pytest.mark.asyncio
async def test_create_sample_type_rejects_duplicate_name():
    sample_type = DomainSampleType(name="Bottled water")
    port = AsyncMock()
    port.get_sample_type_by_name.return_value = DomainSampleType(
        id=SAMPLE_TYPE_ID, name=sample_type.name
    )
    service = TypeService(port)

    with pytest.raises(DuplicateSampleTypeError):
        await service.create_sample_type(sample_type)
    port.save_sample_type.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_sample_types_and_get_by_id_return_items():
    sample_type = DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water")
    port = AsyncMock()
    port.get_sample_types.return_value = [sample_type]
    port.get_sample_type_by_id.return_value = sample_type
    service = TypeService(port)

    assert await service.get_sample_types() == [sample_type]
    assert await service.get_sample_type_by_id(str(SAMPLE_TYPE_ID)) == sample_type


@pytest.mark.asyncio
async def test_get_sample_type_by_id_rejects_missing_item():
    port = AsyncMock()
    port.get_sample_type_by_id.return_value = None
    service = TypeService(port)

    with pytest.raises(MissingSampleTypeError):
        await service.get_sample_type_by_id(str(SAMPLE_TYPE_ID))


@pytest.mark.asyncio
async def test_update_sample_type_changes_name():
    current = DomainSampleType(id=SAMPLE_TYPE_ID, name="Old")
    port = AsyncMock()
    port.get_sample_type_by_id.return_value = current
    port.get_sample_type_by_name_excluding_id.return_value = None
    port.update_sample_type.return_value = current
    service = TypeService(port)

    result = await service.update_sample_type(
        str(SAMPLE_TYPE_ID), DomainSampleType(name="Bottled water")
    )

    assert result.name == "Bottled water"
    port.update_sample_type.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_sample_type_rejects_duplicate_name():
    current = DomainSampleType(id=SAMPLE_TYPE_ID, name="Old")
    port = AsyncMock()
    port.get_sample_type_by_id.return_value = current
    port.get_sample_type_by_name_excluding_id.return_value = DomainSampleType(
        name="Bottled water"
    )
    service = TypeService(port)

    with pytest.raises(DuplicateSampleTypeError):
        await service.update_sample_type(
            str(SAMPLE_TYPE_ID), DomainSampleType(name="Bottled water")
        )
    port.update_sample_type.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_sample_type_deletes_existing_item():
    sample_type = DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water")
    port = AsyncMock()
    port.get_sample_type_by_id.return_value = sample_type
    service = TypeService(port)

    await service.delete_sample_type(str(SAMPLE_TYPE_ID))

    port.delete_sample_type.assert_awaited_once_with(SAMPLE_TYPE_ID)
