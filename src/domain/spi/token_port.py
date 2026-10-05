from abc import ABC, abstractmethod
from uuid import UUID

from domain.model.authenticated_user import AuthenticatedUser
from domain.util.constants import UserRole


class TokenPort(ABC):
    @abstractmethod
    def create_token(self, user_id: UUID, roles: list[UserRole]) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> AuthenticatedUser:
        pass
