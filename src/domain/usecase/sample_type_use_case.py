from uuid import uuid4

from domain.api.sample_type_service_port import SampleTypeServicePort
from domain.exception.sample_type_exception import (
    SampleTypeAlreadyExistsError,
    SampleTypeNotFoundError,
)
from domain.model.sample_type import SampleType
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.sample_type_persistence_port import SampleTypePersistencePort


class SampleTypeUseCase(SampleTypeServicePort):
    def __init__(
        self,
        persistence_port: SampleTypePersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.persistence_port = persistence_port
        self.logger = logger or NullLogger()

    async def create_sample_type(self, sample_type: SampleType) -> SampleType:
        self.logger.info("Creating sample type", name=sample_type.name)
        await self.__validate_name_is_available(sample_type.name)
        if not sample_type.id:
            sample_type.id = uuid4()
        created = await self.persistence_port.save_sample_type(sample_type)
        self.logger.info("Sample type created", sample_type_id=str(created.id))
        return created

    async def get_sample_types(self) -> list[SampleType]:
        self.logger.info("Retrieving sample types")
        sample_types = await self.persistence_port.get_sample_types()
        self.logger.info("Sample types retrieved", count=len(sample_types))
        return sample_types

    async def get_sample_type_by_id(self, sample_type_id: str) -> SampleType:
        self.logger.info("Retrieving sample type", sample_type_id=sample_type_id)
        sample_type = await self.__request_sample_type_by_id(sample_type_id)
        self.logger.info("Sample type retrieved", sample_type_id=str(sample_type.id))
        return sample_type

    async def update_sample_type(
        self, sample_type_id: str, updated_sample_type: SampleType
    ) -> SampleType:
        self.logger.info("Updating sample type", sample_type_id=sample_type_id)
        current = await self.__request_sample_type_by_id(sample_type_id)
        duplicate = await self.persistence_port.get_sample_type_by_name_excluding_id(
            updated_sample_type.name, sample_type_id
        )
        if duplicate:
            self.logger.warning(
                "Sample type already exists", sample_type_id=sample_type_id
            )
            raise SampleTypeAlreadyExistsError()

        current.name = updated_sample_type.name
        updated = await self.persistence_port.update_sample_type(current)
        self.logger.info("Sample type updated", sample_type_id=str(updated.id))
        return updated

    async def delete_sample_type(self, sample_type_id: str) -> None:
        self.logger.info("Deleting sample type", sample_type_id=sample_type_id)
        sample_type = await self.__request_sample_type_by_id(sample_type_id)
        await self.persistence_port.delete_sample_type(sample_type.id)
        self.logger.info("Sample type deleted", sample_type_id=str(sample_type.id))

    async def __validate_name_is_available(self, name: str) -> None:
        if await self.persistence_port.get_sample_type_by_name(name):
            self.logger.warning("Sample type already exists")
            raise SampleTypeAlreadyExistsError()

    async def __request_sample_type_by_id(self, sample_type_id: str) -> SampleType:
        sample_type = await self.persistence_port.get_sample_type_by_id(sample_type_id)
        if sample_type is None:
            self.logger.warning("Sample type not found", sample_type_id=sample_type_id)
            raise SampleTypeNotFoundError()
        return sample_type
