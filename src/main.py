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
from infrastructure.input.rest.analysis_method_controller import (
    router as analysis_method_router,
)
from infrastructure.input.rest.analyte_controller import router as analyte_router
from infrastructure.input.rest.client_controller import router as client_router
from infrastructure.input.rest.criteria_controller import router as criteria_router
from infrastructure.input.rest.exception.exception_handler import (
    analysis_method_already_exists_exception_handler,
    analysis_method_not_found_exception_handler,
    analyte_already_exists_exception_handler,
    analyte_not_found_exception_handler,
    application_request_validation_exception_handler,
    client_already_exists_excepion_handler,
    client_not_found_exception_handler,
    criteria_already_exists_exception_handler,
    criteria_not_found_exception_handler,
    domain_exception_handler,
    request_validation_exception_handler,
    role_already_exists_exception_handler,
    role_not_found_exception_handler,
    sample_already_exists_exception_handler,
    sample_not_found_exception_handler,
    sample_type_already_exists_exception_handler,
    sample_type_not_found_exception_handler,
    test_not_found_exception_handler,
    test_type_already_exists_exception_handler,
    test_type_not_found_exception_handler,
    unexpected_exception_handler,
    user_already_exists_exception_handler,
    user_not_found_exception_handler,
)
from infrastructure.input.rest.role_controller import router as role_router
from infrastructure.input.rest.sample_controller import router as sample_router
from infrastructure.input.rest.sample_type_controller import (
    router as sample_type_router,
)
from infrastructure.input.rest.test_controller import router as test_router
from infrastructure.input.rest.test_type_controller import router as test_type_router
from infrastructure.input.rest.user_controller import router as user_router

app = FastAPI(
    title="Microlab API",
    version="1.0.0",
)

app.include_router(client_router)
app.include_router(analysis_method_router)
app.include_router(test_type_router)
app.include_router(analyte_router)
app.include_router(sample_type_router)
app.include_router(criteria_router)
app.include_router(sample_router)
app.include_router(test_router)
app.include_router(role_router)
app.include_router(user_router)

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
app.add_exception_handler(
    SampleTypeAlreadyExistsError,
    sample_type_already_exists_exception_handler,
)
app.add_exception_handler(
    SampleTypeNotFoundError,
    sample_type_not_found_exception_handler,
)
app.add_exception_handler(
    CriteriaAlreadyExistsError,
    criteria_already_exists_exception_handler,
)
app.add_exception_handler(
    CriteriaNotFoundError,
    criteria_not_found_exception_handler,
)
app.add_exception_handler(
    SampleAlreadyExistsError,
    sample_already_exists_exception_handler,
)
app.add_exception_handler(
    SampleNotFoundError,
    sample_not_found_exception_handler,
)
app.add_exception_handler(TestNotFoundError, test_not_found_exception_handler)
app.add_exception_handler(RoleAlreadyExistsError, role_already_exists_exception_handler)
app.add_exception_handler(RoleNotFoundError, role_not_found_exception_handler)
app.add_exception_handler(UserAlreadyExistsError, user_already_exists_exception_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_exception_handler)
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(Exception, unexpected_exception_handler)
