from uuid import uuid4

from domain.api.client_service_port import ClientServicePort
from domain.exception.client_exception import ClientAlreadyExistsError
from domain.model.client import Client
from domain.spi.client_persistence_port import ClientPersistencePort


class ClientUseCase(ClientServicePort):
    def __init__(self, client_persistence_port: ClientPersistencePort):
        self.client_persistence_port = client_persistence_port

    async def create_client(self, client: Client) -> Client:
        await self.__validate_client(client.email, client.nit)

        if not client.id:
            client.id = uuid4()

        return await self.client_persistence_port.save_client(client)

    async def get_clients(self) -> list[Client]:
        clients = await self.client_persistence_port.get_clients()
        return clients

    async def __validate_client(self, email: str, nit: str) -> None:
        stored_client = await self.client_persistence_port.get_client_by_email_or_nit(
            email, nit
        )
        if stored_client:
            raise ClientAlreadyExistsError()
