from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.analyte_exception import (
    AnalyteAlreadyExistsError as DuplicateAnalyteError,
)
from domain.exception.analyte_exception import (
    AnalyteNotFoundError as MissingAnalyteError,
)
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from domain.model.analyte import Analyte as DomainAnalyte
from domain.model.test_type import TestType as DomainTestType
from domain.usecase.analyte_use_case import AnalyteUseCase as AnalyteService

ANALYTE_ID = UUID("7dc56aee-5530-4df9-896f-c63d8d39f28e")
TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


def analyte(name: str = "pH") -> DomainAnalyte:
    return DomainAnalyte(
        id=ANALYTE_ID,
        name=name,
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical"),
    )


@pytest.mark.asyncio
async def test_create_analyte_validates_test_type_assigns_id_and_saves():
    item = analyte()
    item.id = None
    analyte_port = AsyncMock()
    test_type_port = AsyncMock()
    analyte_port.get_analyte_by_name.return_value = None
    test_type_port.get_test_type_by_id.return_value = item.test_type
    analyte_port.save_analyte.return_value = item
    service = AnalyteService(analyte_port, test_type_port)

    result = await service.create_analyte(item)

    assert result == item
    assert item.id is not None
    test_type_port.get_test_type_by_id.assert_awaited_once_with(str(TEST_TYPE_ID))
    analyte_port.save_analyte.assert_awaited_once_with(item)


@pytest.mark.asyncio
async def test_create_analyte_rejects_duplicate_name():
    item = analyte()
    analyte_port = AsyncMock()
    analyte_port.get_analyte_by_name.return_value = item
    service = AnalyteService(analyte_port, AsyncMock())

    with pytest.raises(DuplicateAnalyteError):
        await service.create_analyte(item)

    analyte_port.save_analyte.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_analyte_rejects_missing_test_type():
    item = analyte()
    analyte_port = AsyncMock()
    test_type_port = AsyncMock()
    analyte_port.get_analyte_by_name.return_value = None
    test_type_port.get_test_type_by_id.return_value = None
    service = AnalyteService(analyte_port, test_type_port)

    with pytest.raises(MissingTestTypeError):
        await service.create_analyte(item)


@pytest.mark.asyncio
async def test_get_analytes_and_get_by_id_return_persisted_items():
    item = analyte()
    analyte_port = AsyncMock()
    analyte_port.get_analytes.return_value = [item]
    analyte_port.get_analyte_by_id.return_value = item
    service = AnalyteService(analyte_port, AsyncMock())

    assert await service.get_analytes() == [item]
    assert await service.get_analyte_by_id(str(ANALYTE_ID)) == item


@pytest.mark.asyncio
async def test_get_analyte_by_id_rejects_missing_item():
    analyte_port = AsyncMock()
    analyte_port.get_analyte_by_id.return_value = None
    service = AnalyteService(analyte_port, AsyncMock())

    with pytest.raises(MissingAnalyteError):
        await service.get_analyte_by_id(str(ANALYTE_ID))


@pytest.mark.asyncio
async def test_update_analyte_updates_name_and_test_type():
    current = analyte("Old")
    updated = analyte("pH")
    analyte_port = AsyncMock()
    test_type_port = AsyncMock()
    analyte_port.get_analyte_by_id.return_value = current
    analyte_port.get_analyte_by_name_excluding_id.return_value = None
    test_type_port.get_test_type_by_id.return_value = updated.test_type
    analyte_port.update_analyte.return_value = current
    service = AnalyteService(analyte_port, test_type_port)

    result = await service.update_analyte(str(ANALYTE_ID), updated)

    assert result.name == "pH"
    assert result.test_type.id == TEST_TYPE_ID
    analyte_port.get_analyte_by_name_excluding_id.assert_awaited_once_with(
        "pH", str(ANALYTE_ID)
    )
    analyte_port.update_analyte.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_analyte_rejects_duplicate_name():
    current = analyte("Old")
    updated = analyte("pH")
    analyte_port = AsyncMock()
    analyte_port.get_analyte_by_id.return_value = current
    analyte_port.get_analyte_by_name_excluding_id.return_value = analyte("pH")
    service = AnalyteService(analyte_port, AsyncMock())

    with pytest.raises(DuplicateAnalyteError):
        await service.update_analyte(str(ANALYTE_ID), updated)

    analyte_port.update_analyte.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_analyte_requires_existing_item():
    item = analyte()
    analyte_port = AsyncMock()
    analyte_port.get_analyte_by_id.return_value = item
    service = AnalyteService(analyte_port, AsyncMock())

    await service.delete_analyte(str(ANALYTE_ID))

    analyte_port.delete_analyte.assert_awaited_once_with(str(ANALYTE_ID))
