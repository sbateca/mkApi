import logging
from typing import Any

from domain.spi.logger_port import LoggerPort


class LoggerAdapter(LoggerPort):
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, extra={"custom_attributes": kwargs})

    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning(message, extra={"custom_attributes": kwargs})

    def error(self, message: str, **kwargs: Any) -> None:
        self.logger.error(message, extra={"custom_attributes": kwargs})

    def exception(self, message: str, **kwargs: Any) -> None:
        self.logger.exception(message, extra={"custom_attributes": kwargs})
