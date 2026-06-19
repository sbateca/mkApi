from abc import ABC, abstractmethod

from domain.model.analysis_method import AnalysisMethod


class AnalysisMethodServicePort(ABC):
    @abstractmethod
    async def create_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        pass

    @abstractmethod
    async def get_analysis_methods(self) -> list[AnalysisMethod]:
        pass

    @abstractmethod
    async def get_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod:
        pass

    @abstractmethod
    async def update_analysis_method(
        self, analysis_method_id: str, updated_analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        pass

    @abstractmethod
    async def delete_analysis_method(self, analysis_method_id: str) -> None:
        pass
