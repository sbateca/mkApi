from abc import ABC, abstractmethod
from uuid import UUID

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
    async def get_analyte_by_name(
        self, name: str, test_type_id: UUID
    ) -> Analyte | None:
        pass

    @abstractmethod
    async def get_analyte_by_name_excluding_id(
        self, name: str, test_type_id: UUID, analyte_id: str
    ) -> Analyte | None:
        pass

    @abstractmethod
    async def update_analyte(self, analyte: Analyte) -> Analyte:
        pass

    @abstractmethod
    async def delete_analyte(self, analyte_id: str) -> None:
        pass
