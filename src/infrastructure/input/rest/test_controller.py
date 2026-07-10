from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteTestRequestDto,
    GetTestByIdRequestDto,
    TestRequestDto,
    UpdateTestRequestDto,
)
from application.dto.response import TestResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.test_handler_interface import TestHandlerInterface
from infrastructure.configuration.dependencies import get_test_handler

router = APIRouter(prefix="/tests", tags=["Tests"])
TestHandlerDependency = Annotated[TestHandlerInterface, Depends(get_test_handler)]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_test_by_id_request(test_id: str) -> GetTestByIdRequestDto:
    try:
        return GetTestByIdRequestDto(test_id=test_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_test_request(
    test_id: str, test: TestRequestDto
) -> UpdateTestRequestDto:
    try:
        return UpdateTestRequestDto(test_id=test_id, test=test)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_test_request(test_id: str) -> DeleteTestRequestDto:
    try:
        return DeleteTestRequestDto(test_id=test_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetTestByIdRequestDependency = Annotated[
    GetTestByIdRequestDto, Depends(build_get_test_by_id_request)
]
UpdateTestRequestDependency = Annotated[
    UpdateTestRequestDto, Depends(build_update_test_request)
]
DeleteTestRequestDependency = Annotated[
    DeleteTestRequestDto, Depends(build_delete_test_request)
]


@router.post("", response_model=TestResponseDto, status_code=201)
async def create_test(
    request: TestRequestDto, handler: TestHandlerDependency
) -> TestResponseDto:
    return await handler.create_test(request)


@router.get("", response_model=list[TestResponseDto], status_code=200)
async def get_tests(handler: TestHandlerDependency) -> list[TestResponseDto]:
    return await handler.get_tests()


@router.get("/{test_id}", response_model=TestResponseDto, status_code=200)
async def get_test_by_id(
    request: GetTestByIdRequestDependency,
    handler: TestHandlerDependency,
) -> TestResponseDto:
    return await handler.get_test_by_id(request)


@router.put("/{test_id}", response_model=TestResponseDto, status_code=200)
async def update_test(
    request: UpdateTestRequestDependency,
    handler: TestHandlerDependency,
) -> TestResponseDto:
    return await handler.update_test(request)


@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    request: DeleteTestRequestDependency,
    handler: TestHandlerDependency,
) -> None:
    return await handler.delete_test(request)
