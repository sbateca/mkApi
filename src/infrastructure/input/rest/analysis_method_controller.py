from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    AnalysisMethodRequestDto,
    DeleteAnalysisMethodRequestDto,
    GetAnalysisMethodByIdRequestDto,
    UpdateAnalysisMethodRequestDto,
)
from application.dto.response import AnalysisMethodResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.analysis_method_handler_interface import (
    AnalysisMethodHandlerInterface,
)
from domain.model.authorization_action import AuthorizationAction
from domain.util.constants import ResourceType
from infrastructure.configuration.dependencies import get_analysis_method_handler
from infrastructure.input.rest.security.authorization import require_permission

router = APIRouter(prefix="/analysis-methods", tags=["Analysis Methods"])

AnalysisMethodHandlerDependency = Annotated[
    AnalysisMethodHandlerInterface,
    Depends(get_analysis_method_handler),
]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    errors = [
        {"field": item["loc"][0], "message": item["msg"]}
        for item in error.errors(include_context=False)
    ]
    return ApplicationRequestValidationError(errors=errors)


def build_get_analysis_method_by_id_request(
    analysis_method_id: str,
) -> GetAnalysisMethodByIdRequestDto:
    try:
        return GetAnalysisMethodByIdRequestDto(analysis_method_id=analysis_method_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_analysis_method_request(
    analysis_method_id: str,
    analysis_method: AnalysisMethodRequestDto,
) -> UpdateAnalysisMethodRequestDto:
    try:
        return UpdateAnalysisMethodRequestDto(
            analysis_method_id=analysis_method_id,
            analysis_method=analysis_method,
        )
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_analysis_method_request(
    analysis_method_id: str,
) -> DeleteAnalysisMethodRequestDto:
    try:
        return DeleteAnalysisMethodRequestDto(analysis_method_id=analysis_method_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetAnalysisMethodByIdRequestDependency = Annotated[
    GetAnalysisMethodByIdRequestDto,
    Depends(build_get_analysis_method_by_id_request),
]
UpdateAnalysisMethodRequestDependency = Annotated[
    UpdateAnalysisMethodRequestDto,
    Depends(build_update_analysis_method_request),
]
DeleteAnalysisMethodRequestDependency = Annotated[
    DeleteAnalysisMethodRequestDto,
    Depends(build_delete_analysis_method_request),
]


@router.post(
    "",
    response_model=AnalysisMethodResponseDto,
    status_code=201,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.CREATE, ResourceType.ANALYSIS_METHOD)
        )
    ],
)
async def create_analysis_method(
    request: AnalysisMethodRequestDto,
    handler: AnalysisMethodHandlerDependency,
) -> AnalysisMethodResponseDto:
    return await handler.create_analysis_method(request)


@router.get(
    "",
    response_model=list[AnalysisMethodResponseDto],
    status_code=200,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.READ, ResourceType.ANALYSIS_METHOD)
        )
    ],
)
async def get_analysis_methods(
    handler: AnalysisMethodHandlerDependency,
) -> list[AnalysisMethodResponseDto]:
    return await handler.get_analysis_methods()


@router.get(
    "/{analysis_method_id}",
    response_model=AnalysisMethodResponseDto,
    status_code=200,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.READ, ResourceType.ANALYSIS_METHOD)
        )
    ],
)
async def get_analysis_method_by_id(
    request: GetAnalysisMethodByIdRequestDependency,
    handler: AnalysisMethodHandlerDependency,
) -> AnalysisMethodResponseDto:
    return await handler.get_analysis_method_by_id(request)


@router.put(
    "/{analysis_method_id}",
    response_model=AnalysisMethodResponseDto,
    status_code=200,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.UPDATE, ResourceType.ANALYSIS_METHOD)
        )
    ],
)
async def update_analysis_method(
    request: UpdateAnalysisMethodRequestDependency,
    handler: AnalysisMethodHandlerDependency,
) -> AnalysisMethodResponseDto:
    return await handler.update_analysis_method(request)


@router.delete(
    "/{analysis_method_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(AuthorizationAction.DELETE, ResourceType.ANALYSIS_METHOD)
        )
    ],
)
async def delete_analysis_method(
    request: DeleteAnalysisMethodRequestDependency,
    handler: AnalysisMethodHandlerDependency,
) -> None:
    return await handler.delete_analysis_method(request)
