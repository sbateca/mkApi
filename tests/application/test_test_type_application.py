from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request import (
    DeleteTestTypeRequestDto,
    GetTestTypeByIdRequestDto,
    UpdateTestTypeRequestDto,
)
from application.dto.request import (
    TestTypeRequestDto as TypeRequestDto,
)
from application.handler.impl.test_type_handler import TestTypeHandler as TypeHandler
from application.mapper.test_type_mapper import TestTypeMapper as TypeMapper
from domain.model.test_type import TestType as DomainTestType

TEST_TYPE_ID = UUID("f03c6e5a-30e0-4cad-9cd4-e18ae306254e")


def test_test_type_mapper_maps_requests_domain_and_responses():
    mapper = TypeMapper()
    request = TypeRequestDto(name="Physical-Chemical")

    domain = mapper.to_test_type(request)
    response = mapper.to_response(
        DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")
    )
    responses = mapper.to_response_list(
        [DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")]
    )
    mapped_id = mapper.to_test_type_id(
        GetTestTypeByIdRequestDto(test_type_id=str(TEST_TYPE_ID))
    )

    assert domain == DomainTestType(name="Physical-Chemical")
    assert response.id == TEST_TYPE_ID
    assert response.name == "Physical-Chemical"
    assert responses == [response]
    assert mapped_id == str(TEST_TYPE_ID)


@pytest.mark.asyncio
async def test_test_type_handler_delegates_all_operations():
    domain = DomainTestType(id=TEST_TYPE_ID, name="Physical-Chemical")
    service = AsyncMock()
    service.create_test_type.return_value = domain
    service.get_test_types.return_value = [domain]
    service.get_test_type_by_id.return_value = domain
    service.update_test_type.return_value = domain
    handler = TypeHandler(TypeMapper(), service)
    body = TypeRequestDto(name="Physical-Chemical")

    created = await handler.create_test_type(body)
    listed = await handler.get_test_types()
    fetched = await handler.get_test_type_by_id(
        GetTestTypeByIdRequestDto(test_type_id=str(TEST_TYPE_ID))
    )
    updated = await handler.update_test_type(
        UpdateTestTypeRequestDto(test_type_id=str(TEST_TYPE_ID), test_type=body)
    )
    deleted = await handler.delete_test_type(
        DeleteTestTypeRequestDto(test_type_id=str(TEST_TYPE_ID))
    )

    assert created.id == TEST_TYPE_ID
    assert listed == [created]
    assert fetched == created
    assert updated == created
    assert deleted is None
    service.create_test_type.assert_awaited_once()
    service.get_test_types.assert_awaited_once()
    service.get_test_type_by_id.assert_awaited_once_with(str(TEST_TYPE_ID))
    service.update_test_type.assert_awaited_once()
    service.delete_test_type.assert_awaited_once_with(str(TEST_TYPE_ID))
