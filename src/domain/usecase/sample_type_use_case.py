from uuid import uuid4

from domain.api.sample_type_service_port import SampleTypeServicePort
from domain.exception.sample_type_exception import (
    SampleTypeAlreadyExistsError,
    SampleTypeNotFoundError,
)
from domain.model.sample_type import SampleType
from domain.spi.sample_type_persistence_port import SampleTypePersistencePort


class SampleTypeUseCase(SampleTypeServicePort):
    def __init__(self, persistence_port: SampleTypePersistencePort):
        self.persistence_port = persistence_port

    async def create_sample_type(self, sample_type: SampleType) -> SampleType:
        await self.__validate_name_is_available(sample_type.name)
        if not sample_type.id:
            sample_type.id = uuid4()
        return await self.persistence_port.save_sample_type(sample_type)

    async def get_sample_types(self) -> list[SampleType]:
        return await self.persistence_port.get_sample_types()

    async def get_sample_type_by_id(self, sample_type_id: str) -> SampleType:
        return await self.__request_sample_type_by_id(sample_type_id)

    async def update_sample_type(
        self, sample_type_id: str, updated_sample_type: SampleType
    ) -> SampleType:
        current = await self.__request_sample_type_by_id(sample_type_id)
        duplicate = await self.persistence_port.get_sample_type_by_name_excluding_id(
            updated_sample_type.name, sample_type_id
        )
        if duplicate:
            raise SampleTypeAlreadyExistsError()

        current.name = updated_sample_type.name
        return await self.persistence_port.update_sample_type(current)

    async def delete_sample_type(self, sample_type_id: str) -> None:
        sample_type = await self.__request_sample_type_by_id(sample_type_id)
        await self.persistence_port.delete_sample_type(sample_type.id)

    async def __validate_name_is_available(self, name: str) -> None:
        if await self.persistence_port.get_sample_type_by_name(name):
            raise SampleTypeAlreadyExistsError()

    async def __request_sample_type_by_id(self, sample_type_id: str) -> SampleType:
        sample_type = await self.persistence_port.get_sample_type_by_id(sample_type_id)
        if sample_type is None:
            raise SampleTypeNotFoundError()
        return sample_type
