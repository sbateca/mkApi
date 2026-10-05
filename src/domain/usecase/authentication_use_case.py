from datetime import UTC, datetime, timedelta

from domain.exception.authentication_exception import AuthenticationError
from domain.model import AuthTokens, LoginData
from domain.spi.authentication_service_port import AuthenticationServicePort
from domain.spi.password_hasher_port import PasswordHasherPort
from domain.spi.refresh_token_persistence_port import RefreshTokenPersistencePort
from domain.spi.refresh_token_port import RefreshTokenPort
from domain.spi.token_port import TokenPort
from domain.spi.user_persistence_port import UserPersistencePort


class AuthenticationUseCase(AuthenticationServicePort):
    def __init__(
        self,
        user_persistence_port: UserPersistencePort,
        token_port: TokenPort,
        password_hasher_port: PasswordHasherPort,
        refresh_token_persistence_port: RefreshTokenPersistencePort,
        refresh_token_port: RefreshTokenPort,
        refresh_token_expiration_seconds: int,
    ):
        self.user_persistence_port = user_persistence_port
        self.token_port = token_port
        self.password_hasher_port = password_hasher_port
        self.refresh_token_persistence_port = refresh_token_persistence_port
        self.refresh_token_port = refresh_token_port
        self.refresh_token_expiration_seconds = refresh_token_expiration_seconds

    async def login(self, login_data: LoginData) -> AuthTokens:
        user = await self.user_persistence_port.find_by_username(login_data.username)
        if not user:
            raise AuthenticationError()

        if not self.password_hasher_port.verify(login_data.password, user.password):
            raise AuthenticationError()

        return await self._issue_tokens(user)

    async def refresh(self, refresh_token: str) -> AuthTokens:
        new_refresh_token = self.refresh_token_port.generate()
        user_id = await self.refresh_token_persistence_port.rotate(
            self.refresh_token_port.digest(refresh_token),
            self.refresh_token_port.digest(new_refresh_token),
            self._refresh_token_expiration(),
        )
        if not user_id:
            raise AuthenticationError()

        user = await self.user_persistence_port.find_by_id(str(user_id))
        if not user:
            raise AuthenticationError()

        roles = [role.name for role in user.roles]
        access_token = self.token_port.create_token(user.id, roles)
        return AuthTokens(access_token, new_refresh_token)

    async def logout(self, refresh_token: str) -> None:
        await self.refresh_token_persistence_port.revoke(
            self.refresh_token_port.digest(refresh_token)
        )

    async def _issue_tokens(self, user) -> AuthTokens:
        roles = [role.name for role in user.roles]
        access_token = self.token_port.create_token(user.id, roles)
        refresh_token = self.refresh_token_port.generate()
        await self.refresh_token_persistence_port.save(
            self.refresh_token_port.digest(refresh_token),
            user.id,
            self._refresh_token_expiration(),
        )
        return AuthTokens(access_token, refresh_token)

    def _refresh_token_expiration(self) -> datetime:
        return datetime.now(UTC) + timedelta(
            seconds=self.refresh_token_expiration_seconds
        )
