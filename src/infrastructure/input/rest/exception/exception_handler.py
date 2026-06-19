from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.util.constants import REQUEST_VALIDATION_FAILED_TEXT_MESSAGE
from domain.exception.analysis_method_exception import (
    AnalysisMethodAlreadyExistsError,
    AnalysisMethodNotFoundError,
)
from domain.exception.client_exception import (
    ClientAlreadyExistsError,
    ClientNotFoundError,
)
from domain.exception.domain_exception import DomainError
from domain.util.constants import (
    ANALYSIS_METHOD_ALREADY_EXISTS_ERROR_MESSAGE,
    CLIENT_ALREADY_EXISTS_ERROR_MESSAGE,
    DOMAIN_ERROR_MESSAGE,
    UNEXPECTED_ERROR_MESSAGE,
)
from infrastructure.util.constants import (
    AnalysisMethodErrorType,
    ClientErrorType,
    DomainErrorType,
    UnexpectedErrorType,
)


async def analysis_method_already_exists_exception_handler(
    request: Request, exception: AnalysisMethodAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": AnalysisMethodErrorType.ANALYSIS_METHOD_ALREADY_EXISTS.value,
            "message": (
                f"{ANALYSIS_METHOD_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}"
            ),
        },
    )


async def analysis_method_not_found_exception_handler(
    request: Request, exception: AnalysisMethodNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": AnalysisMethodErrorType.ANALYSIS_METHOD_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def request_validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    errors = []

    for error in exception.errors():
        field = ".".join(
            str(location)
            for location in error["loc"]
            if location not in ["body", "path", "query"]
        )

        errors.append(
            {
                "field": field,
                "message": error["msg"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "code": "VALIDATION_ERROR",
            "message": REQUEST_VALIDATION_FAILED_TEXT_MESSAGE,
            "errors": errors,
        },
    )


async def client_already_exists_excepion_handler(
    request: Request, exception: ClientAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": ClientErrorType.CLIENT_ALREADY_EXISTS.value,
            "message": f"{CLIENT_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def client_not_found_exception_handler(
    request: Request, exception: ClientNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": ClientErrorType.CLIENT_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def domain_exception_handler(
    request: Request, exception: DomainError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "type": DomainErrorType.DOMAIN_ERROR.value,
            "message": f"{DOMAIN_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def unexpected_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "type": UnexpectedErrorType.UNEXPECTED_ERROR.value,
            "message": f"{UNEXPECTED_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def application_request_validation_exception_handler(
    request: Request,
    exception: ApplicationRequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "code": "VALIDATION_ERROR",
            "message": REQUEST_VALIDATION_FAILED_TEXT_MESSAGE,
            "errors": exception.errors,
        },
    )
