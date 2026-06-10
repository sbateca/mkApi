from application.util.constants import REQUEST_VALIDATION_FAILED_TEXT_MESSAGE


class ApplicationRequestValidationError(Exception):
    def __init__(self, errors: list[dict]):
        self.errors = errors
        super().__init__(REQUEST_VALIDATION_FAILED_TEXT_MESSAGE)
