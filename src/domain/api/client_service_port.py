from abc import ABC, abstractmethod

from domain.model.client import Client


class ClientServicePort(ABC):
    @abstractmethod
    async def create_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    async def get_clients(self) -> list[Client]:
        pass

    @abstractmethod
    async def get_client_by_id(self, client_id: str) -> Client:
        pass

    @abstractmethod
    async def update_client(self, client_id: str, updated_client: Client) -> Client:
        pass
