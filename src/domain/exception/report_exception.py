from domain.exception.domain_exception import DomainError


class ReportNotFoundError(DomainError):
    def __init__(self):
        super().__init__("The report was not found.")


class ReportSampleConsistencyError(DomainError):
    def __init__(self):
        super().__init__("Every report test must belong to the report sample.")
