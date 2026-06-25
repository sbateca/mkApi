from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteSampleRequestDto,
    GetSampleByIdRequestDto,
    SampleRequestDto,
    UpdateSampleRequestDto,
)
from application.dto.response import SampleResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.sample_handler_interface import SampleHandlerInterface
from infrastructure.configuration.dependencies import get_sample_handler

router = APIRouter(prefix="/samples", tags=["Samples"])
SampleHandlerDependency = Annotated[SampleHandlerInterface, Depends(get_sample_handler)]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_sample_by_id_request(sample_id: str) -> GetSampleByIdRequestDto:
    try:
        return GetSampleByIdRequestDto(sample_id=sample_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_sample_request(
    sample_id: str, sample: SampleRequestDto
) -> UpdateSampleRequestDto:
    try:
        return UpdateSampleRequestDto(sample_id=sample_id, sample=sample)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_sample_request(sample_id: str) -> DeleteSampleRequestDto:
    try:
        return DeleteSampleRequestDto(sample_id=sample_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetSampleByIdRequestDependency = Annotated[
    GetSampleByIdRequestDto, Depends(build_get_sample_by_id_request)
]
UpdateSampleRequestDependency = Annotated[
    UpdateSampleRequestDto, Depends(build_update_sample_request)
]
DeleteSampleRequestDependency = Annotated[
    DeleteSampleRequestDto, Depends(build_delete_sample_request)
]


@router.post("", response_model=SampleResponseDto, status_code=201)
async def create_sample(
    request: SampleRequestDto, handler: SampleHandlerDependency
) -> SampleResponseDto:
    return await handler.create_sample(request)


@router.get("", response_model=list[SampleResponseDto], status_code=200)
async def get_samples(handler: SampleHandlerDependency) -> list[SampleResponseDto]:
    return await handler.get_samples()


@router.get("/{sample_id}", response_model=SampleResponseDto, status_code=200)
async def get_sample_by_id(
    request: GetSampleByIdRequestDependency,
    handler: SampleHandlerDependency,
) -> SampleResponseDto:
    return await handler.get_sample_by_id(request)


@router.put("/{sample_id}", response_model=SampleResponseDto, status_code=200)
async def update_sample(
    request: UpdateSampleRequestDependency,
    handler: SampleHandlerDependency,
) -> SampleResponseDto:
    return await handler.update_sample(request)


@router.delete("/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sample(
    request: DeleteSampleRequestDependency,
    handler: SampleHandlerDependency,
) -> None:
    return await handler.delete_sample(request)
