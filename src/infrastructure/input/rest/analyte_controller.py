from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    AnalyteRequestDto,
    DeleteAnalyteRequestDto,
    GetAnalyteByIdRequestDto,
    UpdateAnalyteRequestDto,
)
from application.dto.response import AnalyteResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.analyte_handler_interface import AnalyteHandlerInterface
from infrastructure.configuration.dependencies import get_analyte_handler

router = APIRouter(prefix="/analytes", tags=["Analytes"])
AnalyteHandlerDependency = Annotated[
    AnalyteHandlerInterface, Depends(get_analyte_handler)
]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_analyte_by_id_request(analyte_id: str) -> GetAnalyteByIdRequestDto:
    try:
        return GetAnalyteByIdRequestDto(analyte_id=analyte_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_analyte_request(
    analyte_id: str, analyte: AnalyteRequestDto
) -> UpdateAnalyteRequestDto:
    try:
        return UpdateAnalyteRequestDto(analyte_id=analyte_id, analyte=analyte)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_analyte_request(analyte_id: str) -> DeleteAnalyteRequestDto:
    try:
        return DeleteAnalyteRequestDto(analyte_id=analyte_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetAnalyteByIdRequestDependency = Annotated[
    GetAnalyteByIdRequestDto, Depends(build_get_analyte_by_id_request)
]
UpdateAnalyteRequestDependency = Annotated[
    UpdateAnalyteRequestDto, Depends(build_update_analyte_request)
]
DeleteAnalyteRequestDependency = Annotated[
    DeleteAnalyteRequestDto, Depends(build_delete_analyte_request)
]


@router.post("", response_model=AnalyteResponseDto, status_code=201)
async def create_analyte(
    request: AnalyteRequestDto, handler: AnalyteHandlerDependency
) -> AnalyteResponseDto:
    return await handler.create_analyte(request)


@router.get("", response_model=list[AnalyteResponseDto], status_code=200)
async def get_analytes(
    handler: AnalyteHandlerDependency,
) -> list[AnalyteResponseDto]:
    return await handler.get_analytes()


@router.get("/{analyte_id}", response_model=AnalyteResponseDto, status_code=200)
async def get_analyte_by_id(
    request: GetAnalyteByIdRequestDependency,
    handler: AnalyteHandlerDependency,
) -> AnalyteResponseDto:
    return await handler.get_analyte_by_id(request)


@router.put("/{analyte_id}", response_model=AnalyteResponseDto, status_code=200)
async def update_analyte(
    request: UpdateAnalyteRequestDependency,
    handler: AnalyteHandlerDependency,
) -> AnalyteResponseDto:
    return await handler.update_analyte(request)


@router.delete("/{analyte_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analyte(
    request: DeleteAnalyteRequestDependency,
    handler: AnalyteHandlerDependency,
) -> None:
    return await handler.delete_analyte(request)
