from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from domain.exception.client_exception import (
    ClientAlreadyExistsError,
    ClientNotFoundError,
)
from domain.exception.domain_exception import DomainError
from infrastructure.input.rest.client_controller import router as client_router
from infrastructure.input.rest.exception.exception_handler import (
    client_already_exists_excepion_handler,
    client_not_found_exception_handler,
    domain_exception_handler,
    request_validation_exception_handler,
    unexpected_exception_handler,
)

app = FastAPI(
    title="Microlab API",
    version="1.0.0",
)

app.include_router(client_router)


app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,
)
app.add_exception_handler(
    ClientAlreadyExistsError, client_already_exists_excepion_handler
)
app.add_exception_handler(ClientNotFoundError, client_not_found_exception_handler)
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(Exception, unexpected_exception_handler)
