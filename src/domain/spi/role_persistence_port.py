from abc import ABC, abstractmethod

from domain.model.role import Role


class RolePersistencePort(ABC):
    @abstractmethod
    async def save(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def find_by_id(self, role_id: str) -> Role | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Role]:
        pass

    @abstractmethod
    async def delete(self, role_id: str) -> None:
        pass

    @abstractmethod
    async def update(self, role_id: str, updated_role: Role) -> Role:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Role | None:
        pass

    @abstractmethod
    async def find_roles_by_names(self, names: list[str]) -> list[Role]:
        pass
