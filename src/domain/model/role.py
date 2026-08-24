from dataclasses import dataclass
from uuid import UUID

from domain.util.constants import UserRole


@dataclass
class Role:
    name: UserRole
    id: UUID | None = None
