from uuid import UUID

from fastapi import APIRouter

from application.dto.response.action_response_dto import (
    ActionDecisionResponseDto,
    CollectionActionsResponseDto,
)
from domain.model.action_decision import ActionDecision
from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.policy.action_policy import ActionPolicy
from domain.spi.authorization_port import AuthorizationPort
from domain.util.constants import (
    ACTION_UNSUPPORTED_ERROR_MESSAGE,
    ActionDecisionCode,
    ResourceType,
)
from infrastructure.input.rest.security.authorization import (
    AuthenticatedActor,
    AuthorizationDependency,
)

RESOURCE_ACTIONS = (
    AuthorizationAction.READ,
    AuthorizationAction.UPDATE,
    AuthorizationAction.DELETE,
)


def get_resource_actions(
    actor: AuthenticatedUser,
    authorization: AuthorizationPort,
    resource_type: ResourceType,
    client_id: UUID | None = None,
    *,
    blocked_mutation: ActionDecision | None = None,
) -> dict[str, ActionDecisionResponseDto]:
    policy = ActionPolicy(authorization)
    resource = AuthorizationResource(resource_type, client_id)
    return {
        action.value: ActionDecisionResponseDto.from_decision(
            policy.evaluate_action(
                actor,
                action,
                resource,
                rule=(
                    (lambda: blocked_mutation)
                    if blocked_mutation is not None
                    and action is not AuthorizationAction.READ
                    else None
                ),
            )
        )
        for action in RESOURCE_ACTIONS
    }


def register_collection_actions(
    router: APIRouter, resource_type: ResourceType, *, supports_create: bool = True
) -> None:
    @router.get("/actions", response_model=CollectionActionsResponseDto)
    async def get_collection_actions(
        actor: AuthenticatedActor, authorization: AuthorizationDependency
    ) -> CollectionActionsResponseDto:
        decision = (
            ActionPolicy(authorization).evaluate_action(
                actor, AuthorizationAction.CREATE, AuthorizationResource(resource_type)
            )
            if supports_create
            else ActionDecision(
                allowed=False,
                code=ActionDecisionCode.UNSUPPORTED_ACTION.value,
                reason=ACTION_UNSUPPORTED_ERROR_MESSAGE,
            )
        )
        return CollectionActionsResponseDto(
            create=ActionDecisionResponseDto.from_decision(decision)
        )
