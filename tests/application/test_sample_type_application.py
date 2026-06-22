from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request import (
    DeleteSampleTypeRequestDto,
    GetSampleTypeByIdRequestDto,
    UpdateSampleTypeRequestDto,
)
from application.dto.request import (
    SampleTypeRequestDto as TypeRequestDto,
)
from application.handler.impl.sample_type_handler import (
    SampleTypeHandler as AppHandler,
)
from application.mapper.sample_type_mapper import SampleTypeMapper as AppMapper
from domain.model.sample_type import SampleType as DomainSampleType

SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")


def test_sample_type_mapper_maps_all_shapes():
    mapper = AppMapper()
    request = TypeRequestDto(name="Bottled water")
    domain = DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water")

    assert mapper.to_sample_type(request) == DomainSampleType(name="Bottled water")
    response = mapper.to_response(domain)
    assert response.id == SAMPLE_TYPE_ID
    assert mapper.to_response_list([domain]) == [response]
    assert mapper.to_sample_type_id(
        GetSampleTypeByIdRequestDto(sample_type_id=str(SAMPLE_TYPE_ID))
    ) == str(SAMPLE_TYPE_ID)


@pytest.mark.asyncio
async def test_sample_type_handler_delegates_all_operations():
    domain = DomainSampleType(id=SAMPLE_TYPE_ID, name="Bottled water")
    service = AsyncMock()
    service.create_sample_type.return_value = domain
    service.get_sample_types.return_value = [domain]
    service.get_sample_type_by_id.return_value = domain
    service.update_sample_type.return_value = domain
    handler = AppHandler(AppMapper(), service)
    body = TypeRequestDto(name="Bottled water")

    assert (await handler.create_sample_type(body)).id == SAMPLE_TYPE_ID
    assert len(await handler.get_sample_types()) == 1
    assert (
        await handler.get_sample_type_by_id(
            GetSampleTypeByIdRequestDto(sample_type_id=str(SAMPLE_TYPE_ID))
        )
    ).id == SAMPLE_TYPE_ID
    assert (
        await handler.update_sample_type(
            UpdateSampleTypeRequestDto(
                sample_type_id=str(SAMPLE_TYPE_ID), sample_type=body
            )
        )
    ).id == SAMPLE_TYPE_ID
    assert (
        await handler.delete_sample_type(
            DeleteSampleTypeRequestDto(sample_type_id=str(SAMPLE_TYPE_ID))
        )
        is None
    )
    service.delete_sample_type.assert_awaited_once_with(str(SAMPLE_TYPE_ID))
