from domain.model.client import Client
from domain.spi.client_persistence_port import ClientPersistencePort
from infrastructure.output.postgresql.mapper.client_entity_mapper import (
    ClientEntityMapper,
)
from infrastructure.output.postgresql.repository.client_repository import (
    ClientPostgreSQLRepository,
)


class ClientPersistenceAdapter(ClientPersistencePort):
    def __init__(
        self,
        client_repository: ClientPostgreSQLRepository,
        client_entity_mapper: ClientEntityMapper,
    ):
        self.client_repository = client_repository
        self.client_entity_mapper = client_entity_mapper

    async def get_clients(self) -> list[Client]:
        client_entities = await self.client_repository.get_clients()
        return self.client_entity_mapper.to_domain_list(client_entities)

    async def get_client_by_id(self, client_id: str) -> Client | None:
        client_entity = await self.client_repository.get_client_by_id(client_id)
        if client_entity:
            return self.client_entity_mapper.to_domain(client_entity)
        return None

    async def save_client(self, client: Client) -> Client:
        client_entity = self.client_entity_mapper.to_entity(client)
        saved_client_entity = await self.client_repository.save_client(client_entity)
        return self.client_entity_mapper.to_domain(saved_client_entity)

    async def get_client_by_email_or_nit(self, email: str, nit: str) -> Client | None:
        client_entity = await self.client_repository.get_client_by_email_or_nit(
            email, nit
        )
        if client_entity:
            return self.client_entity_mapper.to_domain(client_entity)
        return None
