from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
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
from domain.exception.domain_exception import DomainError
from domain.exception.test_type_exception import (
    TestTypeAlreadyExistsError,
    TestTypeNotFoundError,
)
from infrastructure.input.rest.analysis_method_controller import (
    router as analysis_method_router,
)
from infrastructure.input.rest.analyte_controller import router as analyte_router
from infrastructure.input.rest.client_controller import router as client_router
from infrastructure.input.rest.exception.exception_handler import (
    analysis_method_already_exists_exception_handler,
    analysis_method_not_found_exception_handler,
    analyte_already_exists_exception_handler,
    analyte_not_found_exception_handler,
    application_request_validation_exception_handler,
    client_already_exists_excepion_handler,
    client_not_found_exception_handler,
    domain_exception_handler,
    request_validation_exception_handler,
    test_type_already_exists_exception_handler,
    test_type_not_found_exception_handler,
    unexpected_exception_handler,
)
from infrastructure.input.rest.test_type_controller import router as test_type_router

app = FastAPI(
    title="Microlab API",
    version="1.0.0",
)

app.include_router(client_router)
app.include_router(analysis_method_router)
app.include_router(test_type_router)
app.include_router(analyte_router)

app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,
)

app.add_exception_handler(
    ApplicationRequestValidationError,
    application_request_validation_exception_handler,
)
app.add_exception_handler(
    ClientAlreadyExistsError, client_already_exists_excepion_handler
)
app.add_exception_handler(ClientNotFoundError, client_not_found_exception_handler)
app.add_exception_handler(
    AnalysisMethodAlreadyExistsError,
    analysis_method_already_exists_exception_handler,
)
app.add_exception_handler(
    AnalysisMethodNotFoundError,
    analysis_method_not_found_exception_handler,
)
app.add_exception_handler(
    TestTypeAlreadyExistsError,
    test_type_already_exists_exception_handler,
)
app.add_exception_handler(
    TestTypeNotFoundError,
    test_type_not_found_exception_handler,
)
app.add_exception_handler(
    AnalyteAlreadyExistsError,
    analyte_already_exists_exception_handler,
)
app.add_exception_handler(AnalyteNotFoundError, analyte_not_found_exception_handler)
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(Exception, unexpected_exception_handler)
