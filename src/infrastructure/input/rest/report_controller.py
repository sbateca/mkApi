from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteReportRequestDto,
    GetReportByIdRequestDto,
    ReportRequestDto,
    UpdateReportRequestDto,
)
from application.dto.request.set_report_status_request_dto import (
    SetReportStatusRequestDto,
)
from application.dto.response import ReportResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.report_handler_interface import ReportHandlerInterface
from domain.model.authorization_action import AuthorizationAction
from domain.util.constants import ReportStatus, ResourceType
from infrastructure.configuration.dependencies import get_report_handler
from infrastructure.input.rest.security.authorization import (
    AuthenticatedActor,
    AuthorizationDependency,
    ensure_permission,
    require_permission,
)

router = APIRouter(prefix="/reports", tags=["Reports"])
ReportHandlerDependency = Annotated[ReportHandlerInterface, Depends(get_report_handler)]


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_report_by_id_request(report_id: str) -> GetReportByIdRequestDto:
    try:
        return GetReportByIdRequestDto(report_id=report_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_report_request(
    report_id: str, report: ReportRequestDto
) -> UpdateReportRequestDto:
    try:
        return UpdateReportRequestDto(report_id=report_id, report=report)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_report_request(report_id: str) -> DeleteReportRequestDto:
    try:
        return DeleteReportRequestDto(report_id=report_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_approve_report_request(report_id: str) -> SetReportStatusRequestDto:
    try:
        return SetReportStatusRequestDto(
            reportId=report_id,
            status=ReportStatus.APPROVED.value,
        )
    except ValueError as error:
        raise _validation_error(error) from error


GetReportByIdRequestDependency = Annotated[
    GetReportByIdRequestDto, Depends(build_get_report_by_id_request)
]
UpdateReportRequestDependency = Annotated[
    UpdateReportRequestDto, Depends(build_update_report_request)
]
DeleteReportRequestDependency = Annotated[
    DeleteReportRequestDto, Depends(build_delete_report_request)
]
ApproveReportRequestDependency = Annotated[
    SetReportStatusRequestDto, Depends(build_approve_report_request)
]


@router.post(
    "",
    response_model=ReportResponseDto,
    status_code=201,
    dependencies=[
        Depends(require_permission(AuthorizationAction.CREATE, ResourceType.REPORT))
    ],
)
async def create_report(
    request: ReportRequestDto, handler: ReportHandlerDependency
) -> ReportResponseDto:
    return await handler.create_report(request)


@router.get(
    "",
    response_model=list[ReportResponseDto],
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.REPORT))
    ],
)
async def get_reports(
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> list[ReportResponseDto]:
    return await handler.get_reports(actor)


@router.get(
    "/{report_id}",
    response_model=ReportResponseDto,
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.REPORT))
    ],
)
async def get_report_by_id(
    request: GetReportByIdRequestDependency,
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
    authorization: AuthorizationDependency,
) -> ReportResponseDto:
    report = await handler.get_report_by_id(request)
    ensure_permission(
        actor,
        authorization,
        AuthorizationAction.READ,
        ResourceType.REPORT,
        report.sample.client.id,
    )
    return report


@router.put(
    "/{report_id}",
    response_model=ReportResponseDto,
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.UPDATE, ResourceType.REPORT))
    ],
)
async def update_report(
    request: UpdateReportRequestDependency,
    handler: ReportHandlerDependency,
) -> ReportResponseDto:
    return await handler.update_report(request)


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission(AuthorizationAction.DELETE, ResourceType.REPORT))
    ],
)
async def delete_report(
    request: DeleteReportRequestDependency,
    handler: ReportHandlerDependency,
) -> None:
    return await handler.delete_report(request)


@router.patch(
    "/{report_id}/approve",
    response_model=ReportResponseDto,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission(AuthorizationAction.APPROVE, ResourceType.REPORT))
    ],
)
async def approve_report(
    request: ApproveReportRequestDependency,
    handler: ReportHandlerDependency,
) -> ReportResponseDto:
    return await handler.set_report_status(request)
