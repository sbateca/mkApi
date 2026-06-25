from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.client_exception import ClientNotFoundError as MissingClientError
from domain.exception.sample_exception import (
    SampleAlreadyExistsError as DuplicateSampleError,
)
from domain.exception.sample_exception import SampleNotFoundError as MissingSampleError
from domain.exception.sample_type_exception import (
    SampleTypeNotFoundError as MissingSampleTypeError,
)
from domain.model.client import Client as DomainClient
from domain.model.sample import Sample as DomainSample
from domain.model.sample_type import SampleType as DomainSampleType
from domain.usecase.sample_use_case import SampleUseCase as SampleService

SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")
CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")


def sample(sample_code: str = "1001") -> DomainSample:
    return DomainSample(
        id=SAMPLE_ID,
        sample_code=sample_code,
        sample_type=DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water"),
        client=DomainClient(
            id=CLIENT_ID,
            name="Maximum Hotel",
            email="hotel@example.com",
            phone="5551234",
            nit="123456",
            address="Main street",
        ),
        get_sample_date=date(2024, 7, 2),
        reception_date=date(2023, 10, 1),
        analysis_date=date(2023, 10, 2),
        sample_location="Hotel's restaurant",
        responsable="John Lenon",
    )


@pytest.mark.asyncio
async def test_create_sample_validates_relations_assigns_id_and_saves():
    item = sample()
    item.id = None
    sample_port = AsyncMock()
    sample_type_port = AsyncMock()
    client_port = AsyncMock()
    sample_port.get_sample_by_sample_code.return_value = None
    sample_type_port.get_sample_type_by_id.return_value = DomainSampleType(
        id=SAMPLE_TYPE_ID,
        name="Bottled water",
    )
    client_port.get_client_by_id.return_value = DomainClient(
        id=CLIENT_ID,
        name="Maximum Hotel",
        email="hotel@example.com",
        phone="5551234",
        nit="123456",
        address="Main street",
    )
    sample_port.save_sample.return_value = item
    service = SampleService(sample_port, sample_type_port, client_port)

    result = await service.create_sample(item)

    assert result == item
    assert item.id is not None
    sample_type_port.get_sample_type_by_id.assert_awaited_once_with(str(SAMPLE_TYPE_ID))
    client_port.get_client_by_id.assert_awaited_once_with(str(CLIENT_ID))
    sample_port.save_sample.assert_awaited_once_with(item)


@pytest.mark.asyncio
async def test_create_sample_rejects_duplicate_sample_code():
    item = sample()
    sample_port = AsyncMock()
    sample_port.get_sample_by_sample_code.return_value = item
    service = SampleService(sample_port, AsyncMock(), AsyncMock())

    with pytest.raises(DuplicateSampleError):
        await service.create_sample(item)

    sample_port.save_sample.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_sample_rejects_missing_sample_type():
    item = sample()
    sample_port = AsyncMock()
    sample_type_port = AsyncMock()
    sample_port.get_sample_by_sample_code.return_value = None
    sample_type_port.get_sample_type_by_id.return_value = None
    service = SampleService(sample_port, sample_type_port, AsyncMock())

    with pytest.raises(MissingSampleTypeError):
        await service.create_sample(item)


@pytest.mark.asyncio
async def test_create_sample_rejects_missing_client():
    item = sample()
    sample_port = AsyncMock()
    sample_type_port = AsyncMock()
    client_port = AsyncMock()
    sample_port.get_sample_by_sample_code.return_value = None
    sample_type_port.get_sample_type_by_id.return_value = DomainSampleType(
        id=SAMPLE_TYPE_ID,
        name="Bottled water",
    )
    client_port.get_client_by_id.return_value = None
    service = SampleService(sample_port, sample_type_port, client_port)

    with pytest.raises(MissingClientError):
        await service.create_sample(item)


@pytest.mark.asyncio
async def test_get_samples_and_get_by_id_return_persisted_items():
    item = sample()
    sample_port = AsyncMock()
    sample_port.get_samples.return_value = [item]
    sample_port.get_sample_by_id.return_value = item
    service = SampleService(sample_port, AsyncMock(), AsyncMock())

    assert await service.get_samples() == [item]
    assert await service.get_sample_by_id(str(SAMPLE_ID)) == item


@pytest.mark.asyncio
async def test_get_sample_by_id_rejects_missing_item():
    sample_port = AsyncMock()
    sample_port.get_sample_by_id.return_value = None
    service = SampleService(sample_port, AsyncMock(), AsyncMock())

    with pytest.raises(MissingSampleError):
        await service.get_sample_by_id(str(SAMPLE_ID))


@pytest.mark.asyncio
async def test_update_sample_updates_all_fields_and_relations():
    current = sample("old")
    updated = sample("1001")
    sample_port = AsyncMock()
    sample_type_port = AsyncMock()
    client_port = AsyncMock()
    sample_port.get_sample_by_id.return_value = current
    sample_port.get_sample_by_sample_code_excluding_id.return_value = None
    sample_type_port.get_sample_type_by_id.return_value = DomainSampleType(
        id=SAMPLE_TYPE_ID,
        name="Bottled water",
    )
    client_port.get_client_by_id.return_value = DomainClient(
        id=CLIENT_ID,
        name="Maximum Hotel",
        email="hotel@example.com",
        phone="5551234",
        nit="123456",
        address="Main street",
    )
    sample_port.update_sample.return_value = current
    service = SampleService(sample_port, sample_type_port, client_port)

    result = await service.update_sample(str(SAMPLE_ID), updated)

    assert result.sample_code == "1001"
    assert result.sample_type.id == SAMPLE_TYPE_ID
    assert result.client.id == CLIENT_ID
    sample_port.update_sample.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_sample_rejects_duplicate_sample_code():
    current = sample("old")
    updated = sample("1001")
    sample_port = AsyncMock()
    sample_port.get_sample_by_id.return_value = current
    sample_port.get_sample_by_sample_code_excluding_id.return_value = sample("1001")
    service = SampleService(sample_port, AsyncMock(), AsyncMock())

    with pytest.raises(DuplicateSampleError):
        await service.update_sample(str(SAMPLE_ID), updated)

    sample_port.update_sample.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_sample_requires_existing_item():
    item = sample()
    sample_port = AsyncMock()
    sample_port.get_sample_by_id.return_value = item
    service = SampleService(sample_port, AsyncMock(), AsyncMock())

    await service.delete_sample(str(SAMPLE_ID))

    sample_port.delete_sample.assert_awaited_once_with(str(SAMPLE_ID))
