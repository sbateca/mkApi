from dataclasses import dataclass
from uuid import UUID


@dataclass
class SampleType:
    name: str
    id: UUID | None = None
