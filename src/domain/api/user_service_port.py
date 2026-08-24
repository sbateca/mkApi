from abc import ABC, abstractmethod

from domain.model.user import User


class UserServicePort(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_users(self) -> list[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def update_user(self, user_id: str, updated_user: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        pass
