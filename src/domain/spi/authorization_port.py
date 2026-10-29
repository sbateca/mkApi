from abc import ABC, abstractmethod

from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.model.authorization_scope import AuthorizationScope
from domain.util.constants import ResourceType


class AuthorizationPort(ABC):
    @abstractmethod
    def get_scope(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        resource_type: ResourceType,
    ) -> AuthorizationScope:
        pass

    @abstractmethod
    def is_allowed(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        resource: AuthorizationResource,
    ) -> bool:
        pass
