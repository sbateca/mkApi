from uuid import uuid4

from domain.api.analysis_method_service_port import AnalysisMethodServicePort
from domain.exception.analysis_method_exception import (
    AnalysisMethodAlreadyExistsError,
    AnalysisMethodNotFoundError,
)
from domain.model.analysis_method import AnalysisMethod
from domain.spi.analysis_method_persistence_port import AnalysisMethodPersistencePort
from domain.spi.logger_port import LoggerPort, NullLogger


class AnalysisMethodUseCase(AnalysisMethodServicePort):
    def __init__(
        self,
        analysis_method_persistence_port: AnalysisMethodPersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.analysis_method_persistence_port = analysis_method_persistence_port
        self.logger = logger or NullLogger()

    async def create_analysis_method(
        self, analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        self.logger.info("Creating analysis method", name=analysis_method.name)
        await self.__validate_name_is_available(analysis_method.name)

        if not analysis_method.id:
            analysis_method.id = uuid4()

        created = await self.analysis_method_persistence_port.save_analysis_method(
            analysis_method
        )
        self.logger.info("Analysis method created", analysis_method_id=str(created.id))
        return created

    async def get_analysis_methods(self) -> list[AnalysisMethod]:
        self.logger.info("Retrieving analysis methods")
        methods = await self.analysis_method_persistence_port.get_analysis_methods()
        self.logger.info("Analysis methods retrieved", count=len(methods))
        return methods

    async def get_analysis_method_by_id(
        self, analysis_method_id: str
    ) -> AnalysisMethod:
        self.logger.info(
            "Retrieving analysis method", analysis_method_id=analysis_method_id
        )
        method = await self.__request_analysis_method_by_id(analysis_method_id)
        self.logger.info("Analysis method retrieved", analysis_method_id=str(method.id))
        return method

    async def update_analysis_method(
        self, analysis_method_id: str, updated_analysis_method: AnalysisMethod
    ) -> AnalysisMethod:
        self.logger.info(
            "Updating analysis method", analysis_method_id=analysis_method_id
        )
        current_analysis_method = await self.__request_analysis_method_by_id(
            analysis_method_id
        )
        stored_analysis_method = await self.analysis_method_persistence_port.get_analysis_method_by_name_excluding_id(
            updated_analysis_method.name,
            analysis_method_id,
        )
        if stored_analysis_method:
            self.logger.warning(
                "Analysis method already exists",
                analysis_method_id=analysis_method_id,
            )
            raise AnalysisMethodAlreadyExistsError()

        current_analysis_method.name = updated_analysis_method.name
        updated = await self.analysis_method_persistence_port.update_analysis_method(
            current_analysis_method
        )
        self.logger.info("Analysis method updated", analysis_method_id=str(updated.id))
        return updated

    async def delete_analysis_method(self, analysis_method_id: str) -> None:
        self.logger.info(
            "Deleting analysis method", analysis_method_id=analysis_method_id
        )
        analysis_method = await self.__request_analysis_method_by_id(analysis_method_id)
        await self.analysis_method_persistence_port.delete_analysis_method(
            analysis_method.id
        )
        self.logger.info(
            "Analysis method deleted", analysis_method_id=str(analysis_method.id)
        )

    async def __validate_name_is_available(self, name: str) -> None:
        stored_analysis_method = (
            await self.analysis_method_persistence_port.get_analysis_method_by_name(
                name
            )
        )
        if stored_analysis_method:
            self.logger.warning("Analysis method already exists")
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
            self.logger.warning(
                "Analysis method not found", analysis_method_id=analysis_method_id
            )
            raise AnalysisMethodNotFoundError()
        return analysis_method
