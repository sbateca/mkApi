from datetime import date
from uuid import UUID

from domain.model.client import Client as DomainClient
from domain.model.sample import Sample as DomainSample
from domain.model.sample_type import SampleType as DomainSampleType
from infrastructure.output.postgresql.entity.client_entity import (
    ClientEntity,
)
from infrastructure.output.postgresql.entity.sample_entity import (
    SampleEntity as PersistenceEntity,
)
from infrastructure.output.postgresql.entity.sample_type_entity import (
    SampleTypeEntity,
)
from infrastructure.output.postgresql.mapper.client_entity_mapper import (
    ClientEntityMapper,
)
from infrastructure.output.postgresql.mapper.sample_entity_mapper import (
    SampleEntityMapper as PersistenceMapper,
)
from infrastructure.output.postgresql.mapper.sample_type_entity_mapper import (
    SampleTypeEntityMapper,
)

SAMPLE_ID = UUID("7c4972a5-ace8-434e-99cf-f61f21912e4a")

SAMPLE_TYPE_ID = UUID("d52f2988-24a1-4e61-976a-cffe1838025b")

CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")


def sample_mapper() -> PersistenceMapper:
    return PersistenceMapper(SampleTypeEntityMapper(), ClientEntityMapper())


def domain_sample() -> DomainSample:
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
        responsable="John Lenon",
    )


def sample_entity() -> PersistenceEntity:
    entity = PersistenceEntity(
        id=SAMPLE_ID,
        sample_code="1001",
        sample_type_id=SAMPLE_TYPE_ID,
        client_id=CLIENT_ID,
        get_sample_date=date(2024, 7, 2),
        reception_date=date(2023, 10, 1),
        analysis_date=date(2023, 10, 2),
        sample_location="Hotel's restaurant",
        responsable="John Lenon",
    )
    entity.sample_type = SampleTypeEntity(id=SAMPLE_TYPE_ID, name="Bottled water")
    entity.client = ClientEntity(
        id=CLIENT_ID,
        name="Maximum Hotel",
        email="hotel@example.com",
        phone="5551234",
        nit="123456",
        address="Main street",
    )
    return entity
