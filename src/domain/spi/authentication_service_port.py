from abc import ABC, abstractmethod

from domain.model.auth_tokens import AuthTokens
from domain.model.login_data import LoginData


class AuthenticationServicePort(ABC):
    @abstractmethod
    async def login(self, login_data: LoginData) -> AuthTokens:
        pass

    @abstractmethod
    async def refresh(self, refresh_token: str) -> AuthTokens:
        pass

    @abstractmethod
    async def logout(self, refresh_token: str) -> None:
        pass
