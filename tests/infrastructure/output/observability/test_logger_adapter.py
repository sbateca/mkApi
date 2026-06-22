from unittest.mock import MagicMock, patch

from infrastructure.output.observability.logger_adapter import LoggerAdapter


def test_logger_adapter_forwards_all_levels_with_structured_attributes():
    python_logger = MagicMock()
    with patch(
        "infrastructure.output.observability.logger_adapter.logging.getLogger",
        return_value=python_logger,
    ) as get_logger:
        adapter = LoggerAdapter("mkapi.test")

    adapter.info("info", resource_id="1")
    adapter.warning("warning", resource_id="2")
    adapter.error("error", resource_id="3")
    adapter.exception("exception", resource_id="4")

    get_logger.assert_called_once_with("mkapi.test")
    python_logger.info.assert_called_once_with(
        "info", extra={"custom_attributes": {"resource_id": "1"}}
    )
    python_logger.warning.assert_called_once_with(
        "warning", extra={"custom_attributes": {"resource_id": "2"}}
    )
    python_logger.error.assert_called_once_with(
        "error", extra={"custom_attributes": {"resource_id": "3"}}
    )
    python_logger.exception.assert_called_once_with(
        "exception", extra={"custom_attributes": {"resource_id": "4"}}
    )
