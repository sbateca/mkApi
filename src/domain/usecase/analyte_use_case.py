from uuid import uuid4

from domain.api.analyte_service_port import AnalyteServicePort
from domain.exception.analyte_exception import (
    AnalyteAlreadyExistsError,
    AnalyteNotFoundError,
)
from domain.exception.test_type_exception import TestTypeNotFoundError
from domain.model.analyte import Analyte
from domain.model.test_type import TestType
from domain.spi.analyte_persistence_port import AnalytePersistencePort
from domain.spi.test_type_persistence_port import TestTypePersistencePort


class AnalyteUseCase(AnalyteServicePort):
    def __init__(
        self,
        analyte_persistence_port: AnalytePersistencePort,
        test_type_persistence_port: TestTypePersistencePort,
    ):
        self.analyte_persistence_port = analyte_persistence_port
        self.test_type_persistence_port = test_type_persistence_port

    async def create_analyte(self, analyte: Analyte) -> Analyte:
        await self.__validate_name_is_available(analyte.name)
        analyte.test_type = await self.__request_test_type_by_id(
            str(analyte.test_type.id)
        )

        if not analyte.id:
            analyte.id = uuid4()

        new_analyte = await self.analyte_persistence_port.save_analyte(analyte)
        return new_analyte

    async def get_analytes(self) -> list[Analyte]:
        analytes = await self.analyte_persistence_port.get_analytes()
        return analytes

    async def get_analyte_by_id(self, analyte_id: str) -> Analyte:
        analyte = await self.__request_analyte_by_id(analyte_id)
        return analyte

    async def update_analyte(
        self, analyte_id: str, updated_analyte: Analyte
    ) -> Analyte:
        analyte = await self.__request_analyte_by_id(analyte_id)
        stored_analyte = (
            await self.analyte_persistence_port.get_analyte_by_name_excluding_id(
                updated_analyte.name, analyte_id
            )
        )
        if stored_analyte:
            raise AnalyteAlreadyExistsError()

        updated_analyte.test_type = await self.__request_test_type_by_id(
            str(updated_analyte.test_type.id)
        )

        analyte.name = updated_analyte.name
        analyte.test_type = updated_analyte.test_type

        updated_analyte_db = await self.analyte_persistence_port.update_analyte(analyte)
        return updated_analyte_db

    async def delete_analyte(self, analyte_id: str) -> None:
        await self.__request_analyte_by_id(analyte_id)
        await self.analyte_persistence_port.delete_analyte(analyte_id)

    async def __validate_name_is_available(self, name: str) -> None:
        stored_analyte = await self.analyte_persistence_port.get_analyte_by_name(name)
        if stored_analyte:
            raise AnalyteAlreadyExistsError()

    async def __request_analyte_by_id(self, analyte_id: str) -> Analyte:
        analyte = await self.analyte_persistence_port.get_analyte_by_id(analyte_id)
        if analyte is None:
            raise AnalyteNotFoundError()
        return analyte

    async def __request_test_type_by_id(self, test_type_id: str) -> TestType:
        test_type = await self.test_type_persistence_port.get_test_type_by_id(
            test_type_id
        )
        if test_type is None:
            raise TestTypeNotFoundError()
        return test_type
