from dataclasses import dataclass
from uuid import UUID

from domain.model.role import Role


@dataclass
class User:
    name: str
    username: str
    password: str
    email: str
    roles: list[Role]
    id: UUID | None = None
