from abc import ABC, abstractmethod

from domain.model.sample_type import SampleType


class SampleTypeServicePort(ABC):
    @abstractmethod
    async def create_sample_type(self, sample_type: SampleType) -> SampleType:
        pass

    @abstractmethod
    async def get_sample_types(self) -> list[SampleType]:
        pass

    @abstractmethod
    async def get_sample_type_by_id(self, sample_type_id: str) -> SampleType:
        pass

    @abstractmethod
    async def update_sample_type(
        self, sample_type_id: str, updated_sample_type: SampleType
    ) -> SampleType:
        pass

    @abstractmethod
    async def delete_sample_type(self, sample_type_id: str) -> None:
        pass
