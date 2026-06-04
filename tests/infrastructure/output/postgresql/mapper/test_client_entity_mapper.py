from infrastructure.output.postgresql.mapper.client_entity_mapper import (  # type: ignore
    ClientEntityMapper,
)
from tests.builders import ClientBuilder, ClientEntityBuilder


def test_to_entity_maps_domain_model_to_postgresql_entity():
    # Arrange
    client = ClientBuilder().build()
    mapper = ClientEntityMapper()

    # Act
    result = mapper.to_entity(client)

    # Assert
    assert result.id == client.id
    assert result.name == client.name
    assert result.email == client.email
    assert result.phone == client.phone
    assert result.nit == client.nit
    assert result.address == client.address


def test_to_domain_maps_postgresql_entity_to_domain_model():
    # Arrange
    client_entity = ClientEntityBuilder().build()
    mapper = ClientEntityMapper()

    # Act
    result = mapper.to_domain(client_entity)

    # Assert
    assert result.id == client_entity.id
    assert result.name == client_entity.name
    assert result.email == client_entity.email
    assert result.phone == client_entity.phone
    assert result.nit == client_entity.nit
    assert result.address == client_entity.address
