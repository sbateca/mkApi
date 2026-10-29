from pathlib import Path
from uuid import UUID

import pytest

from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.model.authorization_scope import AuthorizationScope
from domain.util.constants import ResourceType, UserRole
from infrastructure.output.authorization.casbin_authorization_adapter import (
    CasbinAuthorizationAdapter,
)

CLIENT_ID = UUID("63cc2808-29d7-4c84-aa9f-feca7792a893")
OTHER_CLIENT_ID = UUID("b078281c-ccee-4f44-a4f4-a05745aa70f3")
USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


@pytest.fixture
def authorization() -> CasbinAuthorizationAdapter:
    policy_directory = (
        Path(__file__).resolve().parents[4]
        / "src"
        / "infrastructure"
        / "output"
        / "authorization"
        / "policies"
    )
    return CasbinAuthorizationAdapter(
        str(policy_directory / "model.conf"),
        str(policy_directory / "policy.csv"),
    )


def actor(role: UserRole, client_id: UUID | None = None) -> AuthenticatedUser:
    return AuthenticatedUser(USER_ID, frozenset({role}), client_id)


@pytest.mark.parametrize(
    ("role", "action", "resource", "allowed"),
    [
        (UserRole.ADMIN, AuthorizationAction.DELETE, ResourceType.USER, True),
        (
            UserRole.TECHNICAL_DIRECTOR,
            AuthorizationAction.APPROVE,
            ResourceType.REPORT,
            True,
        ),
        (
            UserRole.TECHNICAL_DIRECTOR,
            AuthorizationAction.CREATE,
            ResourceType.CLIENT,
            False,
        ),
        (UserRole.ANALYST, AuthorizationAction.CREATE, ResourceType.TEST, True),
        (UserRole.ANALYST, AuthorizationAction.DELETE, ResourceType.TEST, False),
        (UserRole.ANALYST, AuthorizationAction.UPDATE, ResourceType.SAMPLE, True),
        (
            UserRole.ANALYST,
            AuthorizationAction.APPROVE,
            ResourceType.REPORT,
            False,
        ),
        (
            UserRole.RECEPTIONIST,
            AuthorizationAction.CREATE,
            ResourceType.CLIENT,
            True,
        ),
        (
            UserRole.RECEPTIONIST,
            AuthorizationAction.CREATE,
            ResourceType.SAMPLE,
            True,
        ),
        (
            UserRole.RECEPTIONIST,
            AuthorizationAction.UPDATE,
            ResourceType.SAMPLE,
            False,
        ),
        (UserRole.CLIENT, AuthorizationAction.UPDATE, ResourceType.SAMPLE, False),
    ],
)
def test_role_permission_matrix(
    authorization,
    role,
    action,
    resource,
    allowed,
):
    assert (
        authorization.is_allowed(
            actor(role, CLIENT_ID),
            action,
            AuthorizationResource(resource, CLIENT_ID),
        )
        is allowed
    )


def test_client_can_only_read_resources_owned_by_its_client(authorization):
    client = actor(UserRole.CLIENT, CLIENT_ID)

    assert authorization.is_allowed(
        client,
        AuthorizationAction.READ,
        AuthorizationResource(ResourceType.SAMPLE, CLIENT_ID),
    )
    assert not authorization.is_allowed(
        client,
        AuthorizationAction.READ,
        AuthorizationResource(ResourceType.SAMPLE, OTHER_CLIENT_ID),
    )
    assert not authorization.is_allowed(
        actor(UserRole.CLIENT),
        AuthorizationAction.READ,
        AuthorizationResource(ResourceType.SAMPLE, CLIENT_ID),
    )


def test_report_read_scope_reflects_policy(authorization):
    assert (
        authorization.get_scope(
            actor(UserRole.ADMIN),
            AuthorizationAction.READ,
            ResourceType.REPORT,
        )
        is AuthorizationScope.ALL
    )
    assert (
        authorization.get_scope(
            actor(UserRole.CLIENT, CLIENT_ID),
            AuthorizationAction.READ,
            ResourceType.REPORT,
        )
        is AuthorizationScope.OWN
    )
    assert (
        authorization.get_scope(
            actor(UserRole.RECEPTIONIST),
            AuthorizationAction.READ,
            ResourceType.REPORT,
        )
        is AuthorizationScope.DENIED
    )
