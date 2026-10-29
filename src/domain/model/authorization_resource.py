from dataclasses import dataclass
from uuid import UUID

from domain.util.constants import ResourceType


@dataclass(frozen=True)
class AuthorizationResource:
    type: ResourceType
    client_id: UUID | None = None
