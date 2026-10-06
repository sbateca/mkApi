from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from domain.model.sample import Sample
from domain.model.test import Test
from domain.util.constants import ReportStatus


@dataclass
class Report:
    report_number: str
    report_date: date
    status: ReportStatus
    sample: Sample
    tests: list[Test] = field(default_factory=list)
    id: UUID | None = None
