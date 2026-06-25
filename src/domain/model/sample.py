from dataclasses import dataclass
from datetime import date
from uuid import UUID

from domain.model.client import Client
from domain.model.sample_type import SampleType


@dataclass
class Sample:
    sample_code: str
    sample_type: SampleType
    client: Client
    get_sample_date: date
    reception_date: date
    analysis_date: date
    sample_location: str
    responsable: str
    id: UUID | None = None
