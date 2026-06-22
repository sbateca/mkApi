from abc import ABC, abstractmethod
from typing import Any


class LoggerPort(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def exception(self, message: str, **kwargs: Any) -> None:
        pass


class NullLogger(LoggerPort):
    """No-op logger used when a use case is instantiated outside DI."""

    def info(self, message: str, **kwargs: Any) -> None:
        pass

    def warning(self, message: str, **kwargs: Any) -> None:
        pass

    def error(self, message: str, **kwargs: Any) -> None:
        pass

    def exception(self, message: str, **kwargs: Any) -> None:
        pass
