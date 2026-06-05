from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.client_response_dto import ClientResponseDto
from application.handler.client_handler_interface import ClientHandlerInterface
from application.mapper.client_mapper import ClientMapper
from domain.api.client_service_port import ClientServicePort


class ClientHandler(ClientHandlerInterface):
    def __init__(
        self, client_mapper: ClientMapper, client_service_port: ClientServicePort
    ):
        self.client_mapper = client_mapper
        self.client_service_port = client_service_port

    async def get_clients(self) -> list[ClientResponseDto]:
        clients = await self.client_service_port.get_clients()
        return self.client_mapper.to_response_list(clients)

    async def create_client(self, request: CreateClientRequestDto) -> ClientResponseDto:
        client = self.client_mapper.to_client(request)
        created_client = await self.client_service_port.create_client(client)
        return self.client_mapper.to_response(created_client)
