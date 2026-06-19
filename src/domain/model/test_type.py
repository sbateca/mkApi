from dataclasses import dataclass
from uuid import UUID


@dataclass
class TestType:
    name: str
    id: UUID | None = None
