from dataclasses import dataclass
from uuid import UUID

from domain.util.constants import UserRole


@dataclass(frozen=True)
class AuthenticatedUser:
    id: UUID
    roles: frozenset[UserRole]
