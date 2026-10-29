from collections.abc import Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status

from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.spi.authorization_port import AuthorizationPort
from domain.util.constants import ResourceType
from infrastructure.configuration.dependencies import get_authorization_port
from infrastructure.input.rest.security.authentication import get_authenticated_user
from infrastructure.util.constants import AuthenticationErrorType

AuthenticatedActor = Annotated[AuthenticatedUser, Depends(get_authenticated_user)]
AuthorizationDependency = Annotated[
    AuthorizationPort,
    Depends(get_authorization_port),
]


def ensure_permission(
    actor: AuthenticatedUser,
    authorization: AuthorizationPort,
    action: AuthorizationAction,
    resource_type: ResourceType,
    resource_client_id: UUID | None = None,
) -> None:
    if not authorization.is_allowed(
        actor,
        action,
        AuthorizationResource(resource_type, resource_client_id),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=AuthenticationErrorType.INSUFFICIENT_PERMISSIONS.value,
        )


def has_unrestricted_permission(
    actor: AuthenticatedUser,
    authorization: AuthorizationPort,
    action: AuthorizationAction,
    resource_type: ResourceType,
) -> bool:
    return authorization.is_allowed(
        actor,
        action,
        AuthorizationResource(resource_type, UUID(int=0)),
    )


def require_permission(
    action: AuthorizationAction,
    resource_type: ResourceType,
) -> Callable[..., AuthenticatedUser]:
    def authorize(
        actor: AuthenticatedActor,
        authorization: AuthorizationDependency,
    ) -> AuthenticatedUser:
        ensure_permission(actor, authorization, action, resource_type)
        return actor

    return authorize
