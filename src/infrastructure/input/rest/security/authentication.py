from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.model.authenticated_user import AuthenticatedUser
from domain.spi.token_port import TokenPort
from domain.util.constants import UserRole
from infrastructure.configuration.dependencies import get_jwt_adapter
from infrastructure.util.constants import AuthenticationErrorType

bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=AuthenticationErrorType.AUTHENTICATION_REQUIRED.value,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_authenticated_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    token_port: Annotated[TokenPort, Depends(get_jwt_adapter)],
) -> AuthenticatedUser:
    if credentials is None:
        raise _unauthorized()

    try:
        return token_port.decode_token(credentials.credentials)
    except ValueError:
        raise _unauthorized() from None


def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., AuthenticatedUser]:
    def authorize(
        user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    ) -> AuthenticatedUser:
        if user.roles.isdisjoint(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AuthenticationErrorType.INSUFFICIENT_PERMISSIONS.value,
            )
        return user

    return authorize
