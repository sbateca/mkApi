from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.handler.client_handler_interface import ClientHandlerInterface
from application.handler.impl.client_handler import ClientHandler
from application.mapper.client_mapper import ClientMapper
from domain.api.client_service_port import ClientServicePort
from domain.spi.client_persistence_port import ClientPersistencePort
from domain.usecase.client_use_case import ClientUseCase
from infrastructure.output.postgresql.adapter.client_persistence_adapter import (
    ClientPersistenceAdapter,
)
from infrastructure.output.postgresql.database.session import get_db_session
from infrastructure.output.postgresql.mapper.client_entity_mapper import (
    ClientEntityMapper,
)
from infrastructure.output.postgresql.repository.client_repository import (
    ClientPostgreSQLRepository,
)


def get_client_mapper() -> ClientMapper:
    return ClientMapper()


def get_client_entity_mapper() -> ClientEntityMapper:
    return ClientEntityMapper()


def get_client_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ClientPostgreSQLRepository:
    return ClientPostgreSQLRepository(session)


def get_client_persistence_adapter(
    client_repository: Annotated[
        ClientPostgreSQLRepository,
        Depends(get_client_repository),
    ],
    client_entity_mapper: Annotated[
        ClientEntityMapper,
        Depends(get_client_entity_mapper),
    ],
) -> ClientPersistencePort:
    return ClientPersistenceAdapter(
        client_repository=client_repository,
        client_entity_mapper=client_entity_mapper,
    )


def get_client_usecase(
    client_persistence_port: Annotated[
        ClientPersistencePort,
        Depends(get_client_persistence_adapter),
    ],
) -> ClientServicePort:
    return ClientUseCase(
        client_persistence_port=client_persistence_port,
    )


def get_client_handler(
    client_mapper: Annotated[
        ClientMapper,
        Depends(get_client_mapper),
    ],
    client_service_port: Annotated[
        ClientServicePort,
        Depends(get_client_usecase),
    ],
) -> ClientHandlerInterface:
    return ClientHandler(
        client_mapper=client_mapper,
        client_service_port=client_service_port,
    )
