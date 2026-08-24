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
from domain.exception.analyte_exception import (
    AnalyteAlreadyExistsError,
    AnalyteNotFoundError,
)
from domain.exception.client_exception import (
    ClientAlreadyExistsError,
    ClientNotFoundError,
)
from domain.exception.criteria_exception import (
    CriteriaAlreadyExistsError,
    CriteriaNotFoundError,
)
from domain.exception.domain_exception import DomainError
from domain.exception.role_exception import RoleAlreadyExistsError, RoleNotFoundError
from domain.exception.sample_exception import (
    SampleAlreadyExistsError,
    SampleNotFoundError,
)
from domain.exception.sample_type_exception import (
    SampleTypeAlreadyExistsError,
    SampleTypeNotFoundError,
)
from domain.exception.test_exception import TestNotFoundError
from domain.exception.test_type_exception import (
    TestTypeAlreadyExistsError,
    TestTypeNotFoundError,
)
from domain.exception.user_exception import UserAlreadyExistsError, UserNotFoundError
from domain.util.constants import (
    ANALYSIS_METHOD_ALREADY_EXISTS_ERROR_MESSAGE,
    ANALYTE_ALREADY_EXISTS_ERROR_MESSAGE,
    CLIENT_ALREADY_EXISTS_ERROR_MESSAGE,
    CRITERIA_ALREADY_EXISTS_ERROR_MESSAGE,
    DOMAIN_ERROR_MESSAGE,
    SAMPLE_ALREADY_EXISTS_ERROR_MESSAGE,
    SAMPLE_TYPE_ALREADY_EXISTS_ERROR_MESSAGE,
    TEST_TYPE_ALREADY_EXISTS_ERROR_MESSAGE,
    UNEXPECTED_ERROR_MESSAGE,
)
from infrastructure.util.constants import (
    AnalysisMethodErrorType,
    AnalyteErrorType,
    ClientErrorType,
    CriteriaErrorType,
    DomainErrorType,
    RoleErrorType,
    SampleErrorType,
    SampleTypeErrorType,
    TestErrorType,
    TestTypeErrorType,
    UnexpectedErrorType,
    UserErrorType,
)


async def role_already_exists_exception_handler(
    request: Request, exception: RoleAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": RoleErrorType.ROLE_ALREADY_EXISTS.value,
            "message": str(exception),
        },
    )


async def role_not_found_exception_handler(
    request: Request, exception: RoleNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"type": RoleErrorType.ROLE_NOT_FOUND.value, "message": str(exception)},
    )


async def user_already_exists_exception_handler(
    request: Request, exception: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": UserErrorType.USER_ALREADY_EXISTS.value,
            "message": str(exception),
        },
    )


async def user_not_found_exception_handler(
    request: Request, exception: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"type": UserErrorType.USER_NOT_FOUND.value, "message": str(exception)},
    )


async def sample_already_exists_exception_handler(
    request: Request, exception: SampleAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": SampleErrorType.SAMPLE_ALREADY_EXISTS.value,
            "message": f"{SAMPLE_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def sample_not_found_exception_handler(
    request: Request, exception: SampleNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": SampleErrorType.SAMPLE_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def test_not_found_exception_handler(
    request: Request, exception: TestNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": TestErrorType.TEST_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def criteria_already_exists_exception_handler(
    request: Request, exception: CriteriaAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": CriteriaErrorType.CRITERIA_ALREADY_EXISTS.value,
            "message": f"{CRITERIA_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def criteria_not_found_exception_handler(
    request: Request, exception: CriteriaNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": CriteriaErrorType.CRITERIA_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def sample_type_already_exists_exception_handler(
    request: Request, exception: SampleTypeAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": SampleTypeErrorType.SAMPLE_TYPE_ALREADY_EXISTS.value,
            "message": f"{SAMPLE_TYPE_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def sample_type_not_found_exception_handler(
    request: Request, exception: SampleTypeNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": SampleTypeErrorType.SAMPLE_TYPE_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def analyte_already_exists_exception_handler(
    request: Request, exception: AnalyteAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": AnalyteErrorType.ANALYTE_ALREADY_EXISTS.value,
            "message": f"{ANALYTE_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def analyte_not_found_exception_handler(
    request: Request, exception: AnalyteNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": AnalyteErrorType.ANALYTE_NOT_FOUND.value,
            "message": str(exception),
        },
    )


async def test_type_already_exists_exception_handler(
    request: Request, exception: TestTypeAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "type": TestTypeErrorType.TEST_TYPE_ALREADY_EXISTS.value,
            "message": f"{TEST_TYPE_ALREADY_EXISTS_ERROR_MESSAGE}: {str(exception)}",
        },
    )


async def test_type_not_found_exception_handler(
    request: Request, exception: TestTypeNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "type": TestTypeErrorType.TEST_TYPE_NOT_FOUND.value,
            "message": str(exception),
        },
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
