from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

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
from application.dto.response.report_response_dto import (
    ReportCollectionActionsResponseDto,
    ReportWithActionsResponseDto,
)
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.report_handler_interface import ReportHandlerInterface
from domain.exception.report_exception import ReportPdfUnavailableError
from domain.util.constants import ReportStatus
from infrastructure.configuration.dependencies import (
    get_report_handler,
)
from infrastructure.input.rest.security.authorization import (
    AuthenticatedActor,
)
from infrastructure.util.constants import REPORT_PDF_UNAVAILABLE_MESSAGE

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
)
async def create_report(
    request: ReportRequestDto,
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> ReportResponseDto:
    return await handler.create_report(request, actor)


@router.get(
    "",
    response_model=list[ReportWithActionsResponseDto],
    status_code=200,
)
async def get_reports(
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> list[ReportWithActionsResponseDto]:
    return await handler.get_reports(actor)


@router.get("/actions", response_model=ReportCollectionActionsResponseDto)
async def get_report_collection_actions(
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> ReportCollectionActionsResponseDto:
    return handler.get_collection_actions(actor)


@router.get(
    "/{report_id}",
    response_model=ReportWithActionsResponseDto,
    status_code=200,
)
async def get_report_by_id(
    request: GetReportByIdRequestDependency,
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> ReportWithActionsResponseDto:
    return await handler.get_report_by_id(request, actor)


@router.put(
    "/{report_id}",
    response_model=ReportResponseDto,
    status_code=200,
)
async def update_report(
    request: UpdateReportRequestDependency,
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> ReportResponseDto:
    return await handler.update_report(request, actor)


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_report(
    request: DeleteReportRequestDependency,
    actor: AuthenticatedActor,
    handler: ReportHandlerDependency,
) -> None:
    return await handler.delete_report(request, actor)


@router.patch(
    "/{report_id}/approve",
    response_model=ReportResponseDto,
    status_code=status.HTTP_200_OK,
)
async def approve_report(
    request: ApproveReportRequestDependency,
    handler: ReportHandlerDependency,
    actor: AuthenticatedActor,
) -> ReportResponseDto:
    return await handler.set_report_status(request, actor)


@router.get(
    "/{report_id}/download",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}}}},
)
async def download_report(
    request: GetReportByIdRequestDependency,
    actor: AuthenticatedActor,
    handler: ReportHandlerDependency,
) -> Response:
    try:
        pdf = await handler.download_report(request, actor)
    except ReportPdfUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=REPORT_PDF_UNAVAILABLE_MESSAGE,
        ) from error
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="reporte-{request.report_id}.pdf"',
            "Cache-Control": "private, no-store",
        },
    )
