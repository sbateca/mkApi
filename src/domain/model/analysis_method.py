from dataclasses import dataclass
from uuid import UUID


@dataclass
class AnalysisMethod:
    name: str
    id: UUID | None = None
