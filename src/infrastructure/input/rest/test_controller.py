from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from application.dto.request import (
    DeleteTestRequestDto,
    GetTestByIdRequestDto,
    TestRequestDto,
    UpdateTestRequestDto,
)
from application.dto.response import TestResponseDto
from application.dto.response.action_response_dto import ResourceActionsResponseDto
from application.exception.request_validation_error import (
    ApplicationRequestValidationError,
)
from application.handler.test_handler_interface import TestHandlerInterface
from domain.exception.sample_exception import SampleNotFoundError
from domain.model.action_decision import ActionDecision
from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.spi.authorization_port import AuthorizationPort
from domain.spi.sample_persistence_port import SamplePersistencePort
from domain.util.constants import (
    LINKED_REPORT_TEST_ERROR_MESSAGE,
    ActionDecisionCode,
    ResourceType,
)
from infrastructure.configuration.dependencies import (
    get_sample_persistence_adapter,
    get_test_handler,
)
from infrastructure.input.rest.security.authorization import (
    AuthenticatedActor,
    AuthorizationDependency,
    ensure_permission,
    has_unrestricted_permission,
    require_permission,
)
from infrastructure.input.rest.security.resource_actions import (
    get_resource_actions,
    register_collection_actions,
)


class TestWithActionsResponseDto(TestResponseDto, ResourceActionsResponseDto):
    pass


router = APIRouter(prefix="/tests", tags=["Tests"])
register_collection_actions(router, ResourceType.TEST, supports_create=False)
TestHandlerDependency = Annotated[TestHandlerInterface, Depends(get_test_handler)]
SamplePersistenceDependency = Annotated[
    SamplePersistencePort, Depends(get_sample_persistence_adapter)
]


def _with_test_actions(
    test: TestResponseDto,
    actor: AuthenticatedUser,
    authorization: AuthorizationPort,
    client_id: UUID | None,
) -> TestWithActionsResponseDto:
    linked = (
        ActionDecision(
            allowed=False,
            code=ActionDecisionCode.LINKED_REPORT_TEST.value,
            reason=LINKED_REPORT_TEST_ERROR_MESSAGE,
        )
        if test.report_linked
        else None
    )
    return TestWithActionsResponseDto(
        **test.model_dump(),
        actions=get_resource_actions(
            actor, authorization, ResourceType.TEST, client_id, blocked_mutation=linked
        ),
    )


def _validation_error(error: ValueError) -> ApplicationRequestValidationError:
    return ApplicationRequestValidationError(
        errors=[
            {"field": item["loc"][0], "message": item["msg"]}
            for item in error.errors(include_context=False)
        ]
    )


def build_get_test_by_id_request(test_id: str) -> GetTestByIdRequestDto:
    try:
        return GetTestByIdRequestDto(test_id=test_id)
    except ValueError as error:
        raise _validation_error(error) from error


def build_update_test_request(
    test_id: str, test: TestRequestDto
) -> UpdateTestRequestDto:
    try:
        return UpdateTestRequestDto(test_id=test_id, test=test)
    except ValueError as error:
        raise _validation_error(error) from error


def build_delete_test_request(test_id: str) -> DeleteTestRequestDto:
    try:
        return DeleteTestRequestDto(test_id=test_id)
    except ValueError as error:
        raise _validation_error(error) from error


GetTestByIdRequestDependency = Annotated[
    GetTestByIdRequestDto, Depends(build_get_test_by_id_request)
]
UpdateTestRequestDependency = Annotated[
    UpdateTestRequestDto, Depends(build_update_test_request)
]
DeleteTestRequestDependency = Annotated[
    DeleteTestRequestDto, Depends(build_delete_test_request)
]


@router.get(
    "",
    response_model=list[TestWithActionsResponseDto],
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.TEST))
    ],
)
async def get_tests(
    handler: TestHandlerDependency,
    actor: AuthenticatedActor,
    authorization: AuthorizationDependency,
    samples: SamplePersistenceDependency,
) -> list[TestWithActionsResponseDto]:
    tests = await handler.get_tests()
    unrestricted = has_unrestricted_permission(
        actor, authorization, AuthorizationAction.READ, ResourceType.TEST
    )
    authorized_tests = []
    for test in tests:
        client_id = None
        if not unrestricted:
            sample = await samples.get_sample_by_id(test.sample_id)
            if sample is None or not authorization.is_allowed(
                actor,
                AuthorizationAction.READ,
                AuthorizationResource(ResourceType.TEST, sample.client.id),
            ):
                continue
            client_id = sample.client.id
        authorized_tests.append(
            _with_test_actions(test, actor, authorization, client_id)
        )
    return authorized_tests


@router.get(
    "/{test_id}",
    response_model=TestWithActionsResponseDto,
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.READ, ResourceType.TEST))
    ],
)
async def get_test_by_id(
    request: GetTestByIdRequestDependency,
    handler: TestHandlerDependency,
    actor: AuthenticatedActor,
    authorization: AuthorizationDependency,
    samples: SamplePersistenceDependency,
) -> TestWithActionsResponseDto:
    test = await handler.get_test_by_id(request)
    client_id = None
    if not has_unrestricted_permission(
        actor, authorization, AuthorizationAction.READ, ResourceType.TEST
    ):
        sample = await samples.get_sample_by_id(test.sample_id)
        if sample is None:
            raise SampleNotFoundError()
        client_id = sample.client.id
        ensure_permission(
            actor,
            authorization,
            AuthorizationAction.READ,
            ResourceType.TEST,
            client_id,
        )
    return _with_test_actions(test, actor, authorization, client_id)


@router.put(
    "/{test_id}",
    response_model=TestResponseDto,
    status_code=200,
    dependencies=[
        Depends(require_permission(AuthorizationAction.UPDATE, ResourceType.TEST))
    ],
)
async def update_test(
    request: UpdateTestRequestDependency,
    handler: TestHandlerDependency,
) -> TestResponseDto:
    return await handler.update_test(request)


@router.delete(
    "/{test_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission(AuthorizationAction.DELETE, ResourceType.TEST))
    ],
)
async def delete_test(
    request: DeleteTestRequestDependency,
    handler: TestHandlerDependency,
) -> None:
    return await handler.delete_test(request)
