from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from domain.exception.criteria_exception import (
    CriteriaAlreadyExistsError as DuplicateCriteriaError,
)
from domain.exception.criteria_exception import (
    CriteriaNotFoundError as MissingCriteriaError,
)
from domain.model.criteria import Criteria as DomainCriteria
from domain.usecase.criteria_use_case import CriteriaUseCase as CriteriaService

CRITERIA_ID = UUID("b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3")


@pytest.mark.asyncio
async def test_create_criteria_assigns_id_and_saves():
    criteria = DomainCriteria(name="0 UFC/100 ml")
    port = AsyncMock()
    port.get_criteria_by_name.return_value = None
    port.save_criteria.return_value = criteria
    service = CriteriaService(port)

    assert await service.create_criteria(criteria) == criteria
    assert criteria.id is not None
    port.get_criteria_by_name.assert_awaited_once_with("0 UFC/100 ml")
    port.save_criteria.assert_awaited_once_with(criteria)


@pytest.mark.asyncio
async def test_create_criteria_rejects_duplicate_name():
    criteria = DomainCriteria(name="0 UFC/100 ml")
    port = AsyncMock()
    port.get_criteria_by_name.return_value = DomainCriteria(
        id=CRITERIA_ID, name=criteria.name
    )
    service = CriteriaService(port)

    with pytest.raises(DuplicateCriteriaError):
        await service.create_criteria(criteria)
    port.save_criteria.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_criteria_and_get_by_id_return_items():
    criteria = DomainCriteria(id=CRITERIA_ID, name="0 UFC/100 ml")
    port = AsyncMock()
    port.get_criteria.return_value = [criteria]
    port.get_criteria_by_id.return_value = criteria
    service = CriteriaService(port)

    assert await service.get_criteria() == [criteria]
    assert await service.get_criteria_by_id(str(CRITERIA_ID)) == criteria


@pytest.mark.asyncio
async def test_get_criteria_by_id_rejects_missing_item():
    port = AsyncMock()
    port.get_criteria_by_id.return_value = None
    service = CriteriaService(port)

    with pytest.raises(MissingCriteriaError):
        await service.get_criteria_by_id(str(CRITERIA_ID))


@pytest.mark.asyncio
async def test_update_criteria_changes_name():
    current = DomainCriteria(id=CRITERIA_ID, name="Old")
    port = AsyncMock()
    port.get_criteria_by_id.return_value = current
    port.get_criteria_by_name_excluding_id.return_value = None
    port.update_criteria.return_value = current
    service = CriteriaService(port)

    result = await service.update_criteria(
        str(CRITERIA_ID), DomainCriteria(name="0 UFC/100 ml")
    )

    assert result.name == "0 UFC/100 ml"
    port.update_criteria.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_criteria_rejects_duplicate_name():
    current = DomainCriteria(id=CRITERIA_ID, name="Old")
    port = AsyncMock()
    port.get_criteria_by_id.return_value = current
    port.get_criteria_by_name_excluding_id.return_value = DomainCriteria(
        name="0 UFC/100 ml"
    )
    service = CriteriaService(port)

    with pytest.raises(DuplicateCriteriaError):
        await service.update_criteria(
            str(CRITERIA_ID), DomainCriteria(name="0 UFC/100 ml")
        )
    port.update_criteria.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_criteria_deletes_existing_item():
    criteria = DomainCriteria(id=CRITERIA_ID, name="0 UFC/100 ml")
    port = AsyncMock()
    port.get_criteria_by_id.return_value = criteria
    service = CriteriaService(port)

    await service.delete_criteria(str(CRITERIA_ID))

    port.delete_criteria.assert_awaited_once_with(CRITERIA_ID)
