from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.create_client_response_dto import CreateClientResponseDto
from application.handler.client_handler_interface import ClientHandlerInterface
from application.mapper.client_mapper import ClientMapper
from domain.api.client_service_port import ClientServicePort


class ClientHandler(ClientHandlerInterface):
    def __init__(
        self, client_mapper: ClientMapper, client_service_port: ClientServicePort
    ):
        self.client_mapper = client_mapper
        self.client_service_port = client_service_port

    async def create_client(
        self, request: CreateClientRequestDto
    ) -> CreateClientResponseDto:
        client = self.client_mapper.to_client(request)
        created_client = await self.client_service_port.create_client(client)
        return self.client_mapper.to_response(created_client)
