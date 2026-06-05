from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.client_response_dto import ClientResponseDto
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
