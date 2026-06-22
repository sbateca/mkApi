from uuid import uuid4

from domain.api.test_type_service_port import TestTypeServicePort
from domain.exception.test_type_exception import (
    TestTypeAlreadyExistsError,
    TestTypeNotFoundError,
)
from domain.model.test_type import TestType
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.test_type_persistence_port import TestTypePersistencePort


class TestTypeUseCase(TestTypeServicePort):
    def __init__(
        self,
        test_type_persistence_port: TestTypePersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.test_type_persistence_port = test_type_persistence_port
        self.logger = logger or NullLogger()

    async def create_test_type(self, test_type: TestType) -> TestType:
        self.logger.info("Creating test type", name=test_type.name)
        await self.__validate_name_is_available(test_type.name)

        if not test_type.id:
            test_type.id = uuid4()

        created = await self.test_type_persistence_port.save_test_type(test_type)
        self.logger.info("Test type created", test_type_id=str(created.id))
        return created

    async def get_test_types(self) -> list[TestType]:
        self.logger.info("Retrieving test types")
        test_types = await self.test_type_persistence_port.get_test_types()
        self.logger.info("Test types retrieved", count=len(test_types))
        return test_types

    async def get_test_type_by_id(self, test_type_id: str) -> TestType:
        self.logger.info("Retrieving test type", test_type_id=test_type_id)
        test_type = await self.__request_test_type_by_id(test_type_id)
        self.logger.info("Test type retrieved", test_type_id=str(test_type.id))
        return test_type

    async def update_test_type(
        self, test_type_id: str, updated_test_type: TestType
    ) -> TestType:
        self.logger.info("Updating test type", test_type_id=test_type_id)
        current_test_type = await self.__request_test_type_by_id(test_type_id)
        stored_test_type = (
            await self.test_type_persistence_port.get_test_type_by_name_excluding_id(
                updated_test_type.name,
                test_type_id,
            )
        )
        if stored_test_type:
            self.logger.warning("Test type already exists", test_type_id=test_type_id)
            raise TestTypeAlreadyExistsError()

        current_test_type.name = updated_test_type.name
        updated = await self.test_type_persistence_port.update_test_type(
            current_test_type
        )
        self.logger.info("Test type updated", test_type_id=str(updated.id))
        return updated

    async def delete_test_type(self, test_type_id: str) -> None:
        self.logger.info("Deleting test type", test_type_id=test_type_id)
        test_type = await self.__request_test_type_by_id(test_type_id)
        await self.test_type_persistence_port.delete_test_type(test_type.id)
        self.logger.info("Test type deleted", test_type_id=str(test_type.id))

    async def __validate_name_is_available(self, name: str) -> None:
        stored_test_type = await self.test_type_persistence_port.get_test_type_by_name(
            name
        )
        if stored_test_type:
            self.logger.warning("Test type already exists")
            raise TestTypeAlreadyExistsError()

    async def __request_test_type_by_id(self, test_type_id: str) -> TestType:
        test_type = await self.test_type_persistence_port.get_test_type_by_id(
            test_type_id
        )
        if test_type is None:
            self.logger.warning("Test type not found", test_type_id=test_type_id)
            raise TestTypeNotFoundError()
        return test_type
