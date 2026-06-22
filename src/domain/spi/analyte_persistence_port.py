from abc import ABC, abstractmethod

from domain.model.analyte import Analyte


class AnalytePersistencePort(ABC):
    @abstractmethod
    async def save_analyte(self, analyte: Analyte) -> Analyte:
        pass

    @abstractmethod
    async def get_analytes(self) -> list[Analyte]:
        pass

    @abstractmethod
    async def get_analyte_by_id(self, analyte_id: str) -> Analyte | None:
        pass

    @abstractmethod
    async def get_analyte_by_name(self, name: str) -> Analyte | None:
        pass

    @abstractmethod
    async def get_analyte_by_name_excluding_id(
        self, name: str, analyte_id: str
    ) -> Analyte | None:
        pass

    @abstractmethod
    async def update_analyte(self, analyte: Analyte) -> Analyte:
        pass

    @abstractmethod
    async def delete_analyte(self, analyte_id: str) -> None:
        pass
