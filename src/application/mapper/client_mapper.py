from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.client_response_dto import ClientResponseDto
from domain.model.client import Client


class ClientMapper:
    def to_client(self, request: CreateClientRequestDto) -> Client:
        return Client(
            id=None,
            name=request.name,
            email=request.email,
            phone=request.phone,
            nit=request.nit,
            address=request.address,
        )

    def to_response(self, client: Client) -> ClientResponseDto:
        return ClientResponseDto(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            nit=client.nit,
            address=client.address,
        )

    def to_response_list(self, clients: list[Client]) -> list[ClientResponseDto]:
        return [self.to_response(client) for client in clients]
