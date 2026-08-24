from abc import ABC, abstractmethod

from domain.model.role import Role


class RoleServicePort(ABC):
    @abstractmethod
    async def create_role(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def get_roles(self) -> list[Role]:
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: str) -> Role:
        pass

    @abstractmethod
    async def get_role_by_name(self, name: str) -> Role | None:
        pass

    @abstractmethod
    async def find_roles_by_names(self, role_names: list[str]) -> list[Role]:
        pass

    @abstractmethod
    async def update_role(self, role_id: str, updated_role: Role) -> Role:
        pass

    @abstractmethod
    async def delete_role(self, role_id: str) -> None:
        pass
