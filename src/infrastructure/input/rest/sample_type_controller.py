from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteSampleTypeRequestDto,
    GetSampleTypeByIdRequestDto,
    SampleTypeRequestDto,
    UpdateSampleTypeRequestDto,
)
from application.dto.response import SampleTypeResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.sample_type_handler_interface import (
    SampleTypeHandlerInterface,
)
from domain.model.authorization_action import AuthorizationAction
from domain.util.constants import ResourceType
from infrastructure.configuration.dependencies import get_sample_type_handler
from infrastructure.input.rest.security.authorization import require_permission

router = APIRouter(prefix="/sample-types", tags=["Sample Types"])
SampleTypeHandlerDependency = Annotated[
    SampleTypeHandlerInterface, Depends(get_sample_type_handler)
]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_sample_type_by_id_request(
    sample_type_id: str,
) -> GetSampleTypeByIdRequestDto:
    try:
        return GetSampleTypeByIdRequestDto(sample_type_id=sample_type_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_sample_type_request(
    sample_type_id: str, sample_type: SampleTypeRequestDto
) -> UpdateSampleTypeRequestDto:
    try:
        return UpdateSampleTypeRequestDto(
            sample_type_id=sample_type_id, sample_type=sample_type
        )
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_sample_type_request(
    sample_type_id: str,
) -> DeleteSampleTypeRequestDto:
    try:
        return DeleteSampleTypeRequestDto(sample_type_id=sample_type_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetSampleTypeByIdRequestDependency = Annotated[
    GetSampleTypeByIdRequestDto, Depends(build_get_sample_type_by_id_request)
]
UpdateSampleTypeRequestDependency = Annotated[
    UpdateSampleTypeRequestDto, Depends(build_update_sample_type_request)
]
DeleteSampleTypeRequestDependency = Annotated[
    DeleteSampleTypeRequestDto, Depends(build_delete_sample_type_request)
]


@router.post(
    "",
    response_model=SampleTypeResponseDto,
    status_code=201,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.CREATE, ResourceType.SAMPLE_TYPE)
        )
    ],
)
async def create_sample_type(
    request: SampleTypeRequestDto, handler: SampleTypeHandlerDependency
) -> SampleTypeResponseDto:
    return await handler.create_sample_type(request)


@router.get(
    "",
    response_model=list[SampleTypeResponseDto],
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.SAMPLE_TYPE))
    ],
)
async def get_sample_types(
    handler: SampleTypeHandlerDependency,
) -> list[SampleTypeResponseDto]:
    return await handler.get_sample_types()


@router.get(
    "/{sample_type_id}",
    response_model=SampleTypeResponseDto,
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.SAMPLE_TYPE))
    ],
)
async def get_sample_type_by_id(
    request: GetSampleTypeByIdRequestDependency,
    handler: SampleTypeHandlerDependency,
) -> SampleTypeResponseDto:
    return await handler.get_sample_type_by_id(request)


@router.put(
    "/{sample_type_id}",
    response_model=SampleTypeResponseDto,
    status_code=200,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.UPDATE, ResourceType.SAMPLE_TYPE)
        )
    ],
)
async def update_sample_type(
    request: UpdateSampleTypeRequestDependency,
    handler: SampleTypeHandlerDependency,
) -> SampleTypeResponseDto:
    return await handler.update_sample_type(request)


@router.delete(
    "/{sample_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.DELETE, ResourceType.SAMPLE_TYPE)
        )
    ],
)
async def delete_sample_type(
    request: DeleteSampleTypeRequestDependency,
    handler: SampleTypeHandlerDependency,
) -> None:
    return await handler.delete_sample_type(request)
