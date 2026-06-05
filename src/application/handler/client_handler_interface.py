from abc import ABC, abstractmethod

from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.client_response_dto import ClientResponseDto


class ClientHandlerInterface(ABC):
    @abstractmethod
    async def get_clients(self) -> list[ClientResponseDto]:
        pass

    @abstractmethod
    async def create_client(self, request: CreateClientRequestDto) -> ClientResponseDto:
        pass
