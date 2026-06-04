from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request.create_client_request_dto import CreateClientRequestDto
from application.dto.response.create_client_response_dto import CreateClientResponseDto
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
    response_model=CreateClientResponseDto,
    status_code=status.HTTP_201_CREATED,
)
async def create_client(
    request: CreateClientRequestDto,
    handler: ClientHandlerDependency,
) -> CreateClientResponseDto:
    return await handler.create_client(request)
