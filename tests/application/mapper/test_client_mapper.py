from application.mapper.client_mapper import ClientMapper  # type: ignore
from tests.builders import ClientBuilder, CreateClientRequestDtoBuilder


def test_to_client_maps_request_dto_to_domain_model():
    # Arrange
    request = CreateClientRequestDtoBuilder().build()
    mapper = ClientMapper()

    # Act
    result = mapper.to_client(request)

    # Assert
    assert result.id is None
    assert result.name == request.name
    assert result.email == request.email
    assert result.phone == request.phone
    assert result.nit == request.nit
    assert result.address == request.address


def test_to_response_maps_domain_model_to_response_dto():
    # Arrange
    client = ClientBuilder().build()
    mapper = ClientMapper()

    # Act
    result = mapper.to_response(client)

    # Assert
    assert result.id == client.id
    assert result.name == client.name
    assert result.email == client.email
    assert result.phone == client.phone
    assert result.nit == client.nit
    assert result.address == client.address
