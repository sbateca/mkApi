from uuid import uuid4

from domain.api.client_service_port import ClientServicePort
from domain.exception.client_exception import (
    ClientAlreadyExistsError,
    ClientNotFoundError,
)
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

    async def get_client_by_id(self, client_id: str) -> Client:
        client = await self.__request_client_by_id(client_id)
        return client

    async def get_clients(self) -> list[Client]:
        clients = await self.client_persistence_port.get_clients()
        return clients

    async def update_client(self, client_id: str, updated_client: Client) -> Client:
        current_client = await self.__request_client_by_id(client_id)
        await self.__validate_updated_client(
            current_client.id,
            updated_client.email,
            updated_client.nit,
        )

        current_client.name = updated_client.name
        current_client.email = updated_client.email
        current_client.phone = updated_client.phone
        current_client.nit = updated_client.nit
        current_client.address = updated_client.address

        client = await self.client_persistence_port.update_client(current_client)
        return client

    async def delete_client(self, client_id) -> None:
        client = await self.__request_client_by_id(client_id)
        await self.client_persistence_port.delete_client(client.id)

    async def __validate_client(self, email: str, nit: str) -> None:
        stored_client = await self.client_persistence_port.get_client_by_email_or_nit(
            email, nit
        )
        if stored_client:
            raise ClientAlreadyExistsError()

    async def __validate_updated_client(
        self,
        current_client_id: str,
        email: str,
        nit: str,
    ) -> None:
        stored_client = await self.client_persistence_port.get_client_by_email_or_nit_excluding_client_id(
            email, nit, current_client_id
        )
        if stored_client and str(stored_client.id) != str(current_client_id):
            raise ClientAlreadyExistsError()

    async def __request_client_by_id(self, client_id: str) -> Client:
        client = await self.client_persistence_port.get_client_by_id(client_id)
        if client is None:
            raise ClientNotFoundError()
        return client
