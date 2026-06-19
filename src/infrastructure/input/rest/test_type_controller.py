from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteTestTypeRequestDto,
    GetTestTypeByIdRequestDto,
    TestTypeRequestDto,
    UpdateTestTypeRequestDto,
)
from application.dto.response import TestTypeResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.test_type_handler_interface import TestTypeHandlerInterface
from infrastructure.configuration.dependencies import get_test_type_handler

router = APIRouter(prefix="/test-types", tags=["Test Types"])

TestTypeHandlerDependency = Annotated[
    TestTypeHandlerInterface, Depends(get_test_type_handler)
]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    errors = [
        {"field": item["loc"][0], "message": item["msg"]}
        for item in error.errors(include_context=False)
    ]
    return ApplicationRequestValidationError(errors=errors)


def build_get_test_type_by_id_request(
    test_type_id: str,
) -> GetTestTypeByIdRequestDto:
    try:
        return GetTestTypeByIdRequestDto(test_type_id=test_type_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_test_type_request(
    test_type_id: str,
    test_type: TestTypeRequestDto,
) -> UpdateTestTypeRequestDto:
    try:
        return UpdateTestTypeRequestDto(test_type_id=test_type_id, test_type=test_type)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_test_type_request(
    test_type_id: str,
) -> DeleteTestTypeRequestDto:
    try:
        return DeleteTestTypeRequestDto(test_type_id=test_type_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetTestTypeByIdRequestDependency = Annotated[
    GetTestTypeByIdRequestDto, Depends(build_get_test_type_by_id_request)
]
UpdateTestTypeRequestDependency = Annotated[
    UpdateTestTypeRequestDto, Depends(build_update_test_type_request)
]
DeleteTestTypeRequestDependency = Annotated[
    DeleteTestTypeRequestDto, Depends(build_delete_test_type_request)
]


@router.post("", response_model=TestTypeResponseDto, status_code=201)
async def create_test_type(
    request: TestTypeRequestDto, handler: TestTypeHandlerDependency
) -> TestTypeResponseDto:
    return await handler.create_test_type(request)


@router.get("", response_model=list[TestTypeResponseDto], status_code=200)
async def get_test_types(
    handler: TestTypeHandlerDependency,
) -> list[TestTypeResponseDto]:
    return await handler.get_test_types()


@router.get("/{test_type_id}", response_model=TestTypeResponseDto, status_code=200)
async def get_test_type_by_id(
    request: GetTestTypeByIdRequestDependency,
    handler: TestTypeHandlerDependency,
) -> TestTypeResponseDto:
    return await handler.get_test_type_by_id(request)


@router.put("/{test_type_id}", response_model=TestTypeResponseDto, status_code=200)
async def update_test_type(
    request: UpdateTestTypeRequestDependency,
    handler: TestTypeHandlerDependency,
) -> TestTypeResponseDto:
    return await handler.update_test_type(request)


@router.delete("/{test_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_type(
    request: DeleteTestTypeRequestDependency,
    handler: TestTypeHandlerDependency,
) -> None:
    return await handler.delete_test_type(request)
