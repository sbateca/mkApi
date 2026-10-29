from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    ClientRequestDto,
    DeleteClientRequestDto,
    GetClientByIdRequestDto,
    UpdateClientRequestDto,
)
from application.dto.response.client_response_dto import ClientResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.client_handler_interface import ClientHandlerInterface
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.util.constants import ResourceType
from infrastructure.configuration.dependencies import get_client_handler
from infrastructure.input.rest.security.authorization import (
    AuthenticatedActor,
    AuthorizationDependency,
    ensure_permission,
    require_permission,
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


ClientHandlerDependency = Annotated[
    ClientHandlerInterface,
    Depends(get_client_handler),
]


def build_get_client_by_id_request(
    client_id: str,
) -> GetClientByIdRequestDto:
    try:
        return GetClientByIdRequestDto(client_id=client_id)
    except ValueError as error:
        errors = []

        for err in error.errors(include_context=False):
            errors.append(
                {
                    "field": err["loc"][0],
                    "message": err["msg"],
                }
            )

        raise ApplicationRequestValidationError(errors=errors) from error


def build_update_client_request(
    client_id: str,
    client: ClientRequestDto,
) -> UpdateClientRequestDto:
    try:
        return UpdateClientRequestDto(
            client_id=client_id,
            client=client,
        )
    except ValueError as error:
        errors = []

        for err in error.errors(include_context=False):
            errors.append(
                {
                    "field": err["loc"][0],
                    "message": err["msg"],
                }
            )

        raise ApplicationRequestValidationError(errors=errors) from error


def build_delete_client_request(
    client_id: str,
) -> DeleteClientRequestDto:
    try:
        return DeleteClientRequestDto(client_id=client_id)
    except ValueError as error:
        errors = []

        for err in error.errors(include_context=False):
            errors.append(
                {
                    "field": err["loc"][0],
                    "message": err["msg"],
                }
            )

        raise ApplicationRequestValidationError(errors=errors) from error


GetClientByIdRequestDependency = Annotated[
    GetClientByIdRequestDto,
    Depends(build_get_client_by_id_request),
]


UpdateClientRequestDependency = Annotated[
    UpdateClientRequestDto,
    Depends(build_update_client_request),
]

DeleteClientByIdRequestDependency = Annotated[
    DeleteClientRequestDto,
    Depends(build_delete_client_request),
]


@router.post(
    "",
    response_model=ClientResponseDto,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission(AuthorizationAction.CREATE, ResourceType.CLIENT))
    ],
)
async def create_client(
    request: ClientRequestDto,
    handler: ClientHandlerDependency,
) -> ClientResponseDto:
    return await handler.create_client(request)


@router.get(
    "",
    response_model=list[ClientResponseDto],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.CLIENT))
    ],
)
async def get_clients(
    handler: ClientHandlerDependency,
    actor: AuthenticatedActor,
    authorization: AuthorizationDependency,
) -> list[ClientResponseDto]:
    clients = await handler.get_clients()
    return [
        client
        for client in clients
        if authorization.is_allowed(
            actor,
            AuthorizationAction.READ,
            AuthorizationResource(ResourceType.CLIENT, client.id),
        )
    ]


@router.get(
    "/{client_id}",
    response_model=ClientResponseDto,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.CLIENT))
    ],
)
async def get_client_by_id(
    request: GetClientByIdRequestDependency,
    handler: ClientHandlerDependency,
    actor: AuthenticatedActor,
    authorization: AuthorizationDependency,
) -> ClientResponseDto:
    client = await handler.get_client_by_id(request)
    ensure_permission(
        actor,
        authorization,
        AuthorizationAction.READ,
        ResourceType.CLIENT,
        client.id,
    )
    return client


@router.put(
    "/{client_id}",
    response_model=ClientResponseDto,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(AuthorizationAction.UPDATE, ResourceType.CLIENT))
    ],
)
async def update_client(
    request: UpdateClientRequestDependency,
    handler: ClientHandlerDependency,
) -> ClientResponseDto:
    return await handler.update_client(request)


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission(AuthorizationAction.DELETE, ResourceType.CLIENT))
    ],
)
async def delete_client(
    request: DeleteClientByIdRequestDependency,
    handler: ClientHandlerDependency,
) -> None:
    return await handler.delete_client(request)
