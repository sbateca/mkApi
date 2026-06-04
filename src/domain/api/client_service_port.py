from abc import ABC, abstractmethod

from domain.model.client import Client


class ClientServicePort(ABC):
    @abstractmethod
    async def create_client(self, client: Client) -> Client:
        pass
