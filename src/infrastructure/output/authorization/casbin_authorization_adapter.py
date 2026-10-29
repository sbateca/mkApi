from uuid import UUID

import casbin

from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.model.authorization_scope import AuthorizationScope
from domain.spi.authorization_port import AuthorizationPort
from domain.util.constants import ResourceType


class CasbinAuthorizationAdapter(AuthorizationPort):
    def __init__(self, model_path: str, policy_path: str):
        self.enforcer = casbin.Enforcer(model_path, policy_path)

    def get_scope(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        resource_type: ResourceType,
    ) -> AuthorizationScope:
        different_client_id = (
            UUID(int=(actor.client_id.int + 1) % (1 << 128))
            if actor.client_id is not None
            else UUID(int=0)
        )
        if self.is_allowed(
            actor,
            action,
            AuthorizationResource(resource_type, different_client_id),
        ):
            return AuthorizationScope.ALL
        if actor.client_id is not None and self.is_allowed(
            actor,
            action,
            AuthorizationResource(resource_type, actor.client_id),
        ):
            return AuthorizationScope.OWN
        return AuthorizationScope.DENIED

    def is_allowed(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        resource: AuthorizationResource,
    ) -> bool:
        actor_client = str(actor.client_id) if actor.client_id else ""
        resource_client = str(resource.client_id) if resource.client_id else ""
        return any(
            self.enforcer.enforce(
                role.value,
                resource.type.value,
                action.value,
                actor_client,
                resource_client,
            )
            for role in actor.roles
        )
