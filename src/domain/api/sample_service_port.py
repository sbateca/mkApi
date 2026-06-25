from abc import ABC, abstractmethod

from domain.model.sample import Sample


class SampleServicePort(ABC):
    @abstractmethod
    async def create_sample(self, sample: Sample) -> Sample:
        pass

    @abstractmethod
    async def get_samples(self) -> list[Sample]:
        pass

    @abstractmethod
    async def get_sample_by_id(self, sample_id: str) -> Sample:
        pass

    @abstractmethod
    async def update_sample(self, sample_id: str, updated_sample: Sample) -> Sample:
        pass

    @abstractmethod
    async def delete_sample(self, sample_id: str) -> None:
        pass
