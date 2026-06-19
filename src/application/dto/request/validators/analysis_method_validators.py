from uuid import UUID

from application.util.constants import AnalysisMethodRequestError


def validate_analysis_method_id(value: str) -> str:
    analysis_method_id = value.strip()
    if not analysis_method_id:
        raise ValueError(AnalysisMethodRequestError.BLANK_ANALYSIS_METHOD_ID.value)

    try:
        UUID(analysis_method_id)
    except ValueError as error:
        raise ValueError(
            AnalysisMethodRequestError.INVALID_ANALYSIS_METHOD_ID.value
        ) from error

    return analysis_method_id


def validate_analysis_method_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError(AnalysisMethodRequestError.BLANK_NAME.value)
    return name
