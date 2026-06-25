from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from application.dto.request import (
    DeleteSampleRequestDto,
    GetSampleByIdRequestDto,
    SampleRequestDto,
    UpdateSampleRequestDto,
)
from application.handler.impl.sample_handler import SampleHandler as AppHandler
from application.mapper.sample_mapper import SampleMapper as AppMapper
from domain.model.client import Client as DomainClient
from domain.model.sample import Sample as DomainSample
from domain.model.sample_type import SampleType as DomainSampleType

SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")
SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")
CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")


def sample_body() -> SampleRequestDto:
    return SampleRequestDto(
        sampleCode="1001",
        sampleTypeId=str(SAMPLE_TYPE_ID),
        clientId=str(CLIENT_ID),
        getSampleDate="2024-07-02",
        receptionDate="2023-10-01",
        analysisDate="2023-10-02",
        sampleLocation="hotel's restaurant",
        responsable="john lenon",
    )


def sample_domain() -> DomainSample:
    return DomainSample(
        id=SAMPLE_ID,
        sample_code="1001",
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
        responsable="John lenon",
    )


def test_sample_mapper_maps_request_domain_and_nested_response():
    mapper = AppMapper()
    request = sample_body()
    domain = sample_domain()

    mapped = mapper.to_sample(request)
    response = mapper.to_response(domain)

    assert mapped.id is None
    assert mapped.sample_code == "1001"
    assert mapped.sample_type.id == SAMPLE_TYPE_ID
    assert mapped.client.id == CLIENT_ID
    assert mapped.sample_location == "Hotel's restaurant"
    assert response.id == SAMPLE_ID
    assert response.sample_type.name == "Bottled water"
    assert response.client.name == "Maximum Hotel"
    assert response.model_dump(by_alias=True)["sampleCode"] == "1001"
    assert mapper.to_response_list([domain]) == [response]
    assert mapper.to_sample_id(
        GetSampleByIdRequestDto(sample_id=str(SAMPLE_ID))
    ) == str(SAMPLE_ID)


@pytest.mark.asyncio
async def test_sample_handler_delegates_all_operations():
    domain = sample_domain()
    service = AsyncMock()
    service.create_sample.return_value = domain
    service.get_samples.return_value = [domain]
    service.get_sample_by_id.return_value = domain
    service.update_sample.return_value = domain
    handler = AppHandler(AppMapper(), service)
    body = sample_body()

    assert (await handler.create_sample(body)).id == SAMPLE_ID
    assert len(await handler.get_samples()) == 1
    assert (
        await handler.get_sample_by_id(
            GetSampleByIdRequestDto(sample_id=str(SAMPLE_ID))
        )
    ).id == SAMPLE_ID
    assert (
        await handler.update_sample(
            UpdateSampleRequestDto(sample_id=str(SAMPLE_ID), sample=body)
        )
    ).id == SAMPLE_ID
    assert (
        await handler.delete_sample(DeleteSampleRequestDto(sample_id=str(SAMPLE_ID)))
        is None
    )
    service.delete_sample.assert_awaited_once_with(str(SAMPLE_ID))
