from uuid import uuid4

from domain.api.analysis_method_service_port import AnalysisMethodServicePort
from domain.exception.analysis_method_exception import (
    AnalysisMethodAlreadyExistsError,
    AnalysisMethodNotFoundError,
)
from domain.model.analysis_method import AnalysisMethod
from domain.spi.analysis_method_persistence_port import AnalysisMethodPersistencePort


class AnalysisMethodUseCase(AnalysisMethodServicePort):
    def __init__(self, analysis_method_persistence_port: AnalysisMethodPersistencePort):
        self.analysis_method_persistence_port = analysis_method_persistence_port

    async def create_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        await self.__validate_name_is_available(analysis_method.name)

        if not analysis_method.id:
            analysis_method.id = uuid4()

        return await self.analysis_method_persistence_port.save_analysis_method(
            analysis_method
        )

    async def get_analysis_methods(self) -> list[AnalysisMethod]:
        return await self.analysis_method_persistence_port.get_analysis_methods()

    async def get_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod:
        return await self.__request_analysis_method_by_id(analysis_method_id)

    async def update_analysis_method(
        self, analysis_method_id: str, updated_analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        current_analysis_method = await self.__request_analysis_method_by_id(
            analysis_method_id
        )
        stored_analysis_method = await self.analysis_method_persistence_port.get_analysis_method_by_name_excluding_id(
            updated_analysis_method.name,
            analysis_method_id,
        )
        if stored_analysis_method:
            raise AnalysisMethodAlreadyExistsError()

        current_analysis_method.name = updated_analysis_method.name
        return await self.analysis_method_persistence_port.update_analysis_method(
            current_analysis_method
        )

    async def delete_analysis_method(self, analysis_method_id: str) -> None:
        analysis_method = await self.__request_analysis_method_by_id(analysis_method_id)
        await self.analysis_method_persistence_port.delete_analysis_method(
            analysis_method.id
        )

    async def __validate_name_is_available(self, name: str) -> None:
        stored_analysis_method = (
            await self.analysis_method_persistence_port.get_analysis_method_by_name(
                name
            )
        )
        if stored_analysis_method:
            raise AnalysisMethodAlreadyExistsError()

    async def __request_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod:
        analysis_method = (
            await self.analysis_method_persistence_port.get_analysis_method_by_id(
                analysis_method_id
            )
        )
        if analysis_method is None:
            raise AnalysisMethodNotFoundError()
        return analysis_method
