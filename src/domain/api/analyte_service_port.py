from abc import ABC, abstractmethod

from domain.model.analyte import Analyte


class AnalyteServicePort(ABC):
    @abstractmethod
    async def create_analyte(self, analyte: Analyte) -> Analyte:
        pass

    @abstractmethod
    async def get_analytes(self) -> list[Analyte]:
        pass

    @abstractmethod
    async def get_analyte_by_id(self, analyte_id: str) -> Analyte:
        pass

    @abstractmethod
    async def update_analyte(
        self, analyte_id: str, updated_analyte: Analyte
    ) -> Analyte:
        pass

    @abstractmethod
    async def delete_analyte(self, analyte_id: str) -> None:
        pass
