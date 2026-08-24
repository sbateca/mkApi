from abc import ABC, abstractmethod

from domain.model.user import User


class UserPersistencePort(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def update(self, user_id: str, updated_user: User) -> User:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        pass
