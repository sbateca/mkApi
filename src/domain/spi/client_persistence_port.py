from abc import ABC, abstractmethod

from domain.model.client import Client


class ClientPersistencePort(ABC):
    @abstractmethod
    async def save_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    async def get_clients(self) -> list[Client]:
        pass

    @abstractmethod
    async def get_client_by_id(self, client_id: str) -> Client | None:
        pass

    @abstractmethod
    async def update_client(self, updated_client: Client) -> Client:
        pass

    @abstractmethod
    async def get_client_by_email_or_nit(self, email: str, nit: str) -> Client | None:
        pass

    @abstractmethod
    async def get_client_by_email_or_nit_excluding_client_id(
        self, email: str, nit: str, client_id: str
    ) -> Client | None:
        pass
