from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request import CriteriaRequestDto as CriteriaRequestDto
from application.dto.request import (
    DeleteCriteriaRequestDto,
    GetCriteriaByIdRequestDto,
    UpdateCriteriaRequestDto,
)
from application.handler.impl.criteria_handler import CriteriaHandler as AppHandler
from application.mapper.criteria_mapper import CriteriaMapper as AppMapper
from domain.model.criteria import Criteria as DomainCriteria

CRITERIA_ID = UUID("b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3")


def test_criteria_mapper_maps_all_shapes():
    mapper = AppMapper()
    request = CriteriaRequestDto(name="0 UFC/100 ml")
    domain = DomainCriteria(id=CRITERIA_ID, name="0 UFC/100 ml")

    assert mapper.to_criteria(request) == DomainCriteria(name="0 ufc/100 ml")
    response = mapper.to_response(domain)
    assert response.id == CRITERIA_ID
    assert mapper.to_response_list([domain]) == [response]
    assert mapper.to_criteria_id(
        GetCriteriaByIdRequestDto(criteria_id=str(CRITERIA_ID))
    ) == str(CRITERIA_ID)


@pytest.mark.asyncio
async def test_criteria_handler_delegates_all_operations():
    domain = DomainCriteria(id=CRITERIA_ID, name="0 UFC/100 ml")
    service = AsyncMock()
    service.create_criteria.return_value = domain
    service.get_criteria.return_value = [domain]
    service.get_criteria_by_id.return_value = domain
    service.update_criteria.return_value = domain
    handler = AppHandler(AppMapper(), service)
    body = CriteriaRequestDto(name="0 UFC/100 ml")

    assert (await handler.create_criteria(body)).id == CRITERIA_ID
    assert len(await handler.get_criteria()) == 1
    assert (
        await handler.get_criteria_by_id(
            GetCriteriaByIdRequestDto(criteria_id=str(CRITERIA_ID))
        )
    ).id == CRITERIA_ID
    assert (
        await handler.update_criteria(
            UpdateCriteriaRequestDto(criteria_id=str(CRITERIA_ID), criteria=body)
        )
    ).id == CRITERIA_ID
    assert (
        await handler.delete_criteria(
            DeleteCriteriaRequestDto(criteria_id=str(CRITERIA_ID))
        )
        is None
    )
    service.delete_criteria.assert_awaited_once_with(str(CRITERIA_ID))
