from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request import (
    AnalyteRequestDto,
    DeleteAnalyteRequestDto,
    GetAnalyteByIdRequestDto,
    UpdateAnalyteRequestDto,
)
from application.handler.impl.analyte_handler import AnalyteHandler as AppHandler
from application.mapper.analyte_mapper import AnalyteMapper as AppMapper
from domain.model.analyte import Analyte as DomainAnalyte
from domain.model.test_type import TestType as DomainTestType

ANALYTE_ID = UUID("7dc56aee-5530-4df9-896f-c63d8d39f28e")
TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


def test_analyte_mapper_maps_request_domain_and_nested_response():
    mapper = AppMapper()
    request = AnalyteRequestDto(name="pH", test_type_id=str(TEST_TYPE_ID))
    domain = DomainAnalyte(
        id=ANALYTE_ID,
        name="pH",
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical"),
    )

    mapped = mapper.to_analyte(request)
    response = mapper.to_response(domain)

    assert mapped.id is None
    assert mapped.test_type.id == TEST_TYPE_ID
    assert response.id == ANALYTE_ID
    assert response.test_type.name == "Physical-Chemical"
    assert mapper.to_response_list([domain]) == [response]
    assert mapper.to_analyte_id(
        GetAnalyteByIdRequestDto(analyte_id=str(ANALYTE_ID))
    ) == str(ANALYTE_ID)


@pytest.mark.asyncio
async def test_analyte_handler_delegates_all_operations():
    domain = DomainAnalyte(
        id=ANALYTE_ID,
        name="pH",
        test_type=DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical"),
    )
    service = AsyncMock()
    service.create_analyte.return_value = domain
    service.get_analytes.return_value = [domain]
    service.get_analyte_by_id.return_value = domain
    service.update_analyte.return_value = domain
    handler = AppHandler(AppMapper(), service)
    body = AnalyteRequestDto(name="pH", test_type_id=str(TEST_TYPE_ID))

    assert (await handler.create_analyte(body)).id == ANALYTE_ID
    assert len(await handler.get_analytes()) == 1
    assert (
        await handler.get_analyte_by_id(
            GetAnalyteByIdRequestDto(analyte_id=str(ANALYTE_ID))
        )
    ).id == ANALYTE_ID
    assert (
        await handler.update_analyte(
            UpdateAnalyteRequestDto(analyte_id=str(ANALYTE_ID), analyte=body)
        )
    ).id == ANALYTE_ID
    assert (
        await handler.delete_analyte(
            DeleteAnalyteRequestDto(analyte_id=str(ANALYTE_ID))
        )
        is None
    )
    service.delete_analyte.assert_awaited_once_with(str(ANALYTE_ID))
