from abc import ABC, abstractmethod


class RefreshTokenPort(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

    @abstractmethod
    def digest(self, token: str) -> str:
        pass
