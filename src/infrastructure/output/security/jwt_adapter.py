from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import jwt

from domain.model.authenticated_user import AuthenticatedUser
from domain.spi.token_port import TokenPort
from domain.util.constants import UserRole
from infrastructure.util.constants import TokenError, TokenField


class JwtAdapter(TokenPort):
    def __init__(self, secret_key: str, algorithm: str, expiration_time: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_time = expiration_time

    def create_token(self, user_id: UUID, roles: list[UserRole]) -> str:
        now = datetime.now(UTC)
        payload = {
            TokenField.SUB.value: str(user_id),
            TokenField.ROLES.value: [role.value for role in roles],
            TokenField.IAT.value: now,
            TokenField.EXP.value: now + timedelta(seconds=self.expiration_time),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token: str) -> AuthenticatedUser:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return AuthenticatedUser(
                id=UUID(payload[TokenField.SUB.value]),
                roles=frozenset(
                    UserRole(role) for role in payload.get(TokenField.ROLES.value, [])
                ),
            )
        except jwt.ExpiredSignatureError:
            raise ValueError(TokenError.EXPIRED.value) from None
        except (jwt.JWTError, KeyError, TypeError, ValueError):
            raise ValueError(TokenError.INVALID.value) from None
