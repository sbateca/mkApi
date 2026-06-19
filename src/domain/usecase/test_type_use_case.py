from uuid import uuid4

from domain.api.test_type_service_port import TestTypeServicePort
from domain.exception.test_type_exception import (
    TestTypeAlreadyExistsError,
    TestTypeNotFoundError,
)
from domain.model.test_type import TestType
from domain.spi.test_type_persistence_port import TestTypePersistencePort


class TestTypeUseCase(TestTypeServicePort):
    def __init__(self, test_type_persistence_port: TestTypePersistencePort):
        self.test_type_persistence_port = test_type_persistence_port

    async def create_test_type(self, test_type: TestType) -> TestType:
        await self.__validate_name_is_available(test_type.name)

        if not test_type.id:
            test_type.id = uuid4()

        return await self.test_type_persistence_port.save_test_type(test_type)

    async def get_test_types(self) -> list[TestType]:
        return await self.test_type_persistence_port.get_test_types()

    async def get_test_type_by_id(self, test_type_id: str) -> TestType:
        return await self.__request_test_type_by_id(test_type_id)

    async def update_test_type(
        self, test_type_id: str, updated_test_type: TestType
    ) -> TestType:
        current_test_type = await self.__request_test_type_by_id(test_type_id)
        stored_test_type = (
            await self.test_type_persistence_port.get_test_type_by_name_excluding_id(
                updated_test_type.name,
                test_type_id,
            )
        )
        if stored_test_type:
            raise TestTypeAlreadyExistsError()

        current_test_type.name = updated_test_type.name
        return await self.test_type_persistence_port.update_test_type(current_test_type)

    async def delete_test_type(self, test_type_id: str) -> None:
        test_type = await self.__request_test_type_by_id(test_type_id)
        await self.test_type_persistence_port.delete_test_type(test_type.id)

    async def __validate_name_is_available(self, name: str) -> None:
        stored_test_type = await self.test_type_persistence_port.get_test_type_by_name(
            name
        )
        if stored_test_type:
            raise TestTypeAlreadyExistsError()

    async def __request_test_type_by_id(self, test_type_id: str) -> TestType:
        test_type = await self.test_type_persistence_port.get_test_type_by_id(
            test_type_id
        )
        if test_type is None:
            raise TestTypeNotFoundError()
        return test_type
