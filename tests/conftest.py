from uuid import UUID

import pytest

from domain.model.authenticated_user import AuthenticatedUser
from domain.util.constants import UserRole
from infrastructure.input.rest.security.authentication import get_authenticated_user
from main import app


@pytest.fixture(autouse=True)
def authenticated_admin():
    app.dependency_overrides[get_authenticated_user] = lambda: AuthenticatedUser(
        id=UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e"),
        roles=frozenset({UserRole.ADMIN}),
    )
    yield
    app.dependency_overrides.pop(get_authenticated_user, None)
