from domain.model.client import Client
from infrastructure.output.postgresql.entity.client_entity import ClientEntity


class ClientEntityMapper:
    def to_entity(self, client: Client) -> ClientEntity:
        return ClientEntity(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            nit=client.nit,
            address=client.address,
        )

    def to_domain(self, client_entity: ClientEntity) -> Client:
        return Client(
            id=client_entity.id,
            name=client_entity.name,
            email=client_entity.email,
            phone=client_entity.phone,
            nit=client_entity.nit,
            address=client_entity.address,
        )

    def to_domain_list(self, client_entities: list[ClientEntity]) -> list[Client]:
        return [self.to_domain(entity) for entity in client_entities]
