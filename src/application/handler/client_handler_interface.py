from abc import ABC, abstractmethod

from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.create_client_response_dto import CreateClientResponseDto


class ClientHandlerInterface(ABC):
    @abstractmethod
    async def create_client(
        self, request: CreateClientRequestDto
    ) -> CreateClientResponseDto:
        pass
