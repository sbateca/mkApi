from abc import ABC, abstractmethod

from domain.model.sample import Sample


class SamplePersistencePort(ABC):
    @abstractmethod
    async def save_sample(self, sample: Sample) -> Sample:
        pass

    @abstractmethod
    async def get_samples(self) -> list[Sample]:
        pass

    @abstractmethod
    async def get_sample_by_id(self, sample_id: str) -> Sample | None:
        pass

    @abstractmethod
    async def get_sample_by_sample_code(self, sample_code: str) -> Sample | None:
        pass

    @abstractmethod
    async def get_sample_by_sample_code_excluding_id(
        self, sample_code: str, sample_id: str
    ) -> Sample | None:
        pass

    @abstractmethod
    async def update_sample(self, sample: Sample) -> Sample:
        pass

    @abstractmethod
    async def delete_sample(self, sample_id: str) -> None:
        pass
