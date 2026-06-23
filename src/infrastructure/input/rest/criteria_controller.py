from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    CriteriaRequestDto,
    DeleteCriteriaRequestDto,
    GetCriteriaByIdRequestDto,
    UpdateCriteriaRequestDto,
)
from application.dto.response import CriteriaResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.criteria_handler_interface import CriteriaHandlerInterface
from infrastructure.configuration.dependencies import get_criteria_handler

router = APIRouter(prefix="/criteria", tags=["Criteria"])
CriteriaHandlerDependency = Annotated[
    CriteriaHandlerInterface, Depends(get_criteria_handler)
]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_criteria_by_id_request(criteria_id: str) -> GetCriteriaByIdRequestDto:
    try:
        return GetCriteriaByIdRequestDto(criteria_id=criteria_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_criteria_request(
    criteria_id: str, criteria: CriteriaRequestDto
) -> UpdateCriteriaRequestDto:
    try:
        return UpdateCriteriaRequestDto(criteria_id=criteria_id, criteria=criteria)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_criteria_request(criteria_id: str) -> DeleteCriteriaRequestDto:
    try:
        return DeleteCriteriaRequestDto(criteria_id=criteria_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetCriteriaByIdRequestDependency = Annotated[
    GetCriteriaByIdRequestDto, Depends(build_get_criteria_by_id_request)
]
UpdateCriteriaRequestDependency = Annotated[
    UpdateCriteriaRequestDto, Depends(build_update_criteria_request)
]
DeleteCriteriaRequestDependency = Annotated[
    DeleteCriteriaRequestDto, Depends(build_delete_criteria_request)
]


@router.post("", response_model=CriteriaResponseDto, status_code=201)
async def create_criteria(
    request: CriteriaRequestDto, handler: CriteriaHandlerDependency
) -> CriteriaResponseDto:
    return await handler.create_criteria(request)


@router.get("", response_model=list[CriteriaResponseDto], status_code=200)
async def get_criteria(
    handler: CriteriaHandlerDependency,
) -> list[CriteriaResponseDto]:
    return await handler.get_criteria()


@router.get("/{criteria_id}", response_model=CriteriaResponseDto, status_code=200)
async def get_criteria_by_id(
    request: GetCriteriaByIdRequestDependency,
    handler: CriteriaHandlerDependency,
) -> CriteriaResponseDto:
    return await handler.get_criteria_by_id(request)


@router.put("/{criteria_id}", response_model=CriteriaResponseDto, status_code=200)
async def update_criteria(
    request: UpdateCriteriaRequestDependency,
    handler: CriteriaHandlerDependency,
) -> CriteriaResponseDto:
    return await handler.update_criteria(request)


@router.delete("/{criteria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_criteria(
    request: DeleteCriteriaRequestDependency,
    handler: CriteriaHandlerDependency,
) -> None:
    return await handler.delete_criteria(request)
