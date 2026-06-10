from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.request.get_client_by_id_request_dto import GetClientByIdRequestDto
from application.dto.response.client_response_dto import ClientResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.client_handler_interface import ClientHandlerInterface
from infrastructure.configuration.dependencies import get_client_handler

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


GetClientByIdRequestDependency = Annotated[
    GetClientByIdRequestDto,
    Depends(build_get_client_by_id_request),
]


@router.post(
    "",
    response_model=ClientResponseDto,
    status_code=status.HTTP_201_CREATED,
)
async def create_client(
    request: CreateClientRequestDto,
    handler: ClientHandlerDependency,
) -> ClientResponseDto:
    return await handler.create_client(request)


@router.get(
    "",
    response_model=list[ClientResponseDto],
    status_code=status.HTTP_200_OK,
)
async def get_clients(
    handler: ClientHandlerDependency,
) -> list[ClientResponseDto]:
    return await handler.get_clients()


@router.get(
    "/{client_id}",
    response_model=ClientResponseDto,
    status_code=status.HTTP_200_OK,
)
async def get_client_by_id(
    request: GetClientByIdRequestDependency,
    handler: ClientHandlerDependency,
) -> ClientResponseDto:
    return await handler.get_client_by_id(request)
