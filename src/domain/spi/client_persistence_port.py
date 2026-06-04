from abc import ABC, abstractmethod

from domain.model.client import Client


class ClientPersistencePort(ABC):
    @abstractmethod
    async def save_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    async def get_client_by_email_or_nit(self, email: str, nit: str) -> Client | None:
        pass
