from abc import ABC, abstractmethod

from domain.model.sample_type import SampleType


class SampleTypePersistencePort(ABC):
    @abstractmethod
    async def save_sample_type(self, sample_type: SampleType) -> SampleType:
        pass

    @abstractmethod
    async def get_sample_types(self) -> list[SampleType]:
        pass

    @abstractmethod
    async def get_sample_type_by_id(self, sample_type_id: str) -> SampleType | None:
        pass

    @abstractmethod
    async def get_sample_type_by_name(self, name: str) -> SampleType | None:
        pass

    @abstractmethod
    async def get_sample_type_by_name_excluding_id(
        self, name: str, sample_type_id: str
    ) -> SampleType | None:
        pass

    @abstractmethod
    async def update_sample_type(self, sample_type: SampleType) -> SampleType:
        pass

    @abstractmethod
    async def delete_sample_type(self, sample_type_id: str) -> None:
        pass
