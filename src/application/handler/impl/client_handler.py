from application.dto.request.create_client_request_dto import ClientRequestDto
from application.dto.request.get_client_by_id_request_dto import GetClientByIdRequestDto
from application.dto.request.update_client_request_dto import UpdateClientRequestDto
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

    async def get_client_by_id(
        self, request: GetClientByIdRequestDto
    ) -> ClientResponseDto:
        client_id = self.client_mapper.to_client_id(request)
        client = await self.client_service_port.get_client_by_id(client_id)
        return self.client_mapper.to_response(client)

    async def create_client(self, request: ClientRequestDto) -> ClientResponseDto:
        client = self.client_mapper.to_client(request)
        created_client = await self.client_service_port.create_client(client)
        return self.client_mapper.to_response(created_client)

    async def update_client(self, request: UpdateClientRequestDto) -> ClientResponseDto:
        client = self.client_mapper.to_client(request.client)
        updated_client = await self.client_service_port.update_client(
            request.client_id,
            client,
        )
        return self.client_mapper.to_response(updated_client)
