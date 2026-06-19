from abc import ABC, abstractmethod

from domain.model.analysis_method import AnalysisMethod


class AnalysisMethodPersistencePort(ABC):
    @abstractmethod
    async def save_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        pass

    @abstractmethod
    async def get_analysis_methods(self) -> list[AnalysisMethod]:
        pass

    @abstractmethod
    async def get_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod | None:
        pass

    @abstractmethod
    async def get_analysis_method_by_name(self, name: str) -> AnalysisMethod | None:
        pass

    @abstractmethod
    async def get_analysis_method_by_name_excluding_id(
        self, name: str, analysis_method_id: str
    ) -> AnalysisMethod | None:
        pass

    @abstractmethod
    async def update_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        pass

    @abstractmethod
    async def delete_analysis_method(self, analysis_method_id: str) -> None:
        pass
