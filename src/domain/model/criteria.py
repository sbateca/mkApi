from dataclasses import dataclass
from uuid import UUID


@dataclass
class Criteria:
    name: str
    id: UUID | None = None
