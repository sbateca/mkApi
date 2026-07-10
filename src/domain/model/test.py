from dataclasses import dataclass
from uuid import UUID

from domain.model.analysis_method import AnalysisMethod
from domain.model.analyte import Analyte
from domain.model.criteria import Criteria
from domain.model.test_type import TestType


@dataclass
class Test:
    test_type: TestType
    sample_id: str
    analyte: Analyte
    analysis_method: AnalysisMethod
    criteria: Criteria
    result: str
    id: UUID | None = None
