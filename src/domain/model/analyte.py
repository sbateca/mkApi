from dataclasses import dataclass
from uuid import UUID

from domain.model.test_type import TestType


@dataclass
class Analyte:
    name: str
    test_type: TestType
    id: UUID | None = None
