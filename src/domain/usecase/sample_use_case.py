from uuid import uuid4

from domain.api.sample_service_port import SampleServicePort
from domain.exception.client_exception import ClientNotFoundError
from domain.exception.sample_exception import (
    SampleAlreadyExistsError,
    SampleNotFoundError,
)
from domain.exception.sample_type_exception import SampleTypeNotFoundError
from domain.model.client import Client
from domain.model.sample import Sample
from domain.model.sample_type import SampleType
from domain.spi.client_persistence_port import ClientPersistencePort
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.sample_persistence_port import SamplePersistencePort
from domain.spi.sample_type_persistence_port import SampleTypePersistencePort


class SampleUseCase(SampleServicePort):
    def __init__(
        self,
        sample_persistence_port: SamplePersistencePort,
        sample_type_persistence_port: SampleTypePersistencePort,
        client_persistence_port: ClientPersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.sample_persistence_port = sample_persistence_port
        self.sample_type_persistence_port = sample_type_persistence_port
        self.client_persistence_port = client_persistence_port
        self.logger = logger or NullLogger()

    async def create_sample(self, sample: Sample) -> Sample:
        self.logger.info("Creating sample", sample_code=sample.sample_code)
        await self.__validate_sample_code_is_available(sample.sample_code)
        sample.sample_type = await self.__request_sample_type_by_id(
            str(sample.sample_type.id)
        )
        sample.client = await self.__request_client_by_id(str(sample.client.id))

        if not sample.id:
            sample.id = uuid4()

        created = await self.sample_persistence_port.save_sample(sample)
        self.logger.info("Sample created", sample_id=str(created.id))
        return created

    async def get_samples(self) -> list[Sample]:
        self.logger.info("Retrieving samples")
        samples = await self.sample_persistence_port.get_samples()
        self.logger.info("Samples retrieved", count=len(samples))
        return samples

    async def get_sample_by_id(self, sample_id: str) -> Sample:
        self.logger.info("Retrieving sample", sample_id=sample_id)
        sample = await self.__request_sample_by_id(sample_id)
        self.logger.info("Sample retrieved", sample_id=str(sample.id))
        return sample

    async def update_sample(self, sample_id: str, updated_sample: Sample) -> Sample:
        self.logger.info("Updating sample", sample_id=sample_id)
        sample = await self.__request_sample_by_id(sample_id)
        duplicate = (
            await self.sample_persistence_port.get_sample_by_sample_code_excluding_id(
                updated_sample.sample_code, sample_id
            )
        )
        if duplicate:
            self.logger.warning("Sample already exists", sample_id=sample_id)
            raise SampleAlreadyExistsError()

        updated_sample.sample_type = await self.__request_sample_type_by_id(
            str(updated_sample.sample_type.id)
        )
        updated_sample.client = await self.__request_client_by_id(
            str(updated_sample.client.id)
        )

        sample.sample_code = updated_sample.sample_code
        sample.sample_type = updated_sample.sample_type
        sample.client = updated_sample.client
        sample.get_sample_date = updated_sample.get_sample_date
        sample.reception_date = updated_sample.reception_date
        sample.analysis_date = updated_sample.analysis_date
        sample.sample_location = updated_sample.sample_location
        sample.responsable = updated_sample.responsable

        updated = await self.sample_persistence_port.update_sample(sample)
        self.logger.info("Sample updated", sample_id=str(updated.id))
        return updated

    async def delete_sample(self, sample_id: str) -> None:
        self.logger.info("Deleting sample", sample_id=sample_id)
        await self.__request_sample_by_id(sample_id)
        await self.sample_persistence_port.delete_sample(sample_id)
        self.logger.info("Sample deleted", sample_id=sample_id)

    async def __validate_sample_code_is_available(self, sample_code: str) -> None:
        if await self.sample_persistence_port.get_sample_by_sample_code(sample_code):
            self.logger.warning("Sample already exists")
            raise SampleAlreadyExistsError()

    async def __request_sample_by_id(self, sample_id: str) -> Sample:
        sample = await self.sample_persistence_port.get_sample_by_id(sample_id)
        if sample is None:
            self.logger.warning("Sample not found", sample_id=sample_id)
            raise SampleNotFoundError()
        return sample

    async def __request_sample_type_by_id(self, sample_type_id: str) -> SampleType:
        sample_type = await self.sample_type_persistence_port.get_sample_type_by_id(
            sample_type_id
        )
        if sample_type is None:
            self.logger.warning("Sample type not found", sample_type_id=sample_type_id)
            raise SampleTypeNotFoundError()
        return sample_type

    async def __request_client_by_id(self, client_id: str) -> Client:
        client = await self.client_persistence_port.get_client_by_id(client_id)
        if client is None:
            self.logger.warning("Client not found", client_id=client_id)
            raise ClientNotFoundError()
        return client
