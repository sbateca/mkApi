from collections.abc import Callable

from domain.model.action_decision import ActionDecision
from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.spi.authorization_port import AuthorizationPort
from domain.util.constants import ACTION_FORBIDDEN_ERROR_MESSAGE, ActionDecisionCode


class ActionPolicy:
    def __init__(self, authorization_port: AuthorizationPort):
        self.authorization_port = authorization_port

    def evaluate_action(
        self,
        actor: AuthenticatedUser,
        action: AuthorizationAction,
        resource: AuthorizationResource,
        *,
        rule: Callable[[], ActionDecision] | None = None,
    ) -> ActionDecision:
        if not self.authorization_port.is_allowed(actor, action, resource):
            return ActionDecision(
                allowed=False,
                code=ActionDecisionCode.FORBIDDEN.value,
                reason=ACTION_FORBIDDEN_ERROR_MESSAGE,
            )
        if rule is not None:
            return rule()
        return ActionDecision(allowed=True)
