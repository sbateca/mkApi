from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteReportRequestDto,
    GetReportByIdRequestDto,
    ReportRequestDto,
    UpdateReportRequestDto,
)
from application.dto.response import ReportResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.report_handler_interface import ReportHandlerInterface
from infrastructure.configuration.dependencies import get_report_handler

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


GetReportByIdRequestDependency = Annotated[
    GetReportByIdRequestDto, Depends(build_get_report_by_id_request)
]
UpdateReportRequestDependency = Annotated[
    UpdateReportRequestDto, Depends(build_update_report_request)
]
DeleteReportRequestDependency = Annotated[
    DeleteReportRequestDto, Depends(build_delete_report_request)
]


@router.post("", response_model=ReportResponseDto, status_code=201)
async def create_report(
    request: ReportRequestDto, handler: ReportHandlerDependency
) -> ReportResponseDto:
    return await handler.create_report(request)


@router.get("", response_model=list[ReportResponseDto], status_code=200)
async def get_reports(handler: ReportHandlerDependency) -> list[ReportResponseDto]:
    return await handler.get_reports()


@router.get("/{report_id}", response_model=ReportResponseDto, status_code=200)
async def get_report_by_id(
    request: GetReportByIdRequestDependency,
    handler: ReportHandlerDependency,
) -> ReportResponseDto:
    return await handler.get_report_by_id(request)


@router.put("/{report_id}", response_model=ReportResponseDto, status_code=200)
async def update_report(
    request: UpdateReportRequestDependency,
    handler: ReportHandlerDependency,
) -> ReportResponseDto:
    return await handler.update_report(request)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    request: DeleteReportRequestDependency,
    handler: ReportHandlerDependency,
) -> None:
    return await handler.delete_report(request)
