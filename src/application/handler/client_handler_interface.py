from abc import ABC, abstractmethod

from application.dto.request import (
    ClientRequestDto,
    GetClientByIdRequestDto,
    UpdateClientRequestDto,
)
from application.dto.response import ClientResponseDto


class ClientHandlerInterface(ABC):
    @abstractmethod
    async def get_clients(self) -> list[ClientResponseDto]:
        pass

    @abstractmethod
    async def get_client_by_id(
        self, request: GetClientByIdRequestDto
    ) -> ClientResponseDto:
        pass

    @abstractmethod
    async def create_client(self, request: ClientRequestDto) -> ClientResponseDto:
        pass

    @abstractmethod
    async def update_client(self, request: UpdateClientRequestDto) -> ClientResponseDto:
        pass
