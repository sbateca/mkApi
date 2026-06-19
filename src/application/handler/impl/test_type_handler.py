from application.dto.request import (
    DeleteTestTypeRequestDto,
    GetTestTypeByIdRequestDto,
    TestTypeRequestDto,
    UpdateTestTypeRequestDto,
)
from application.dto.response import TestTypeResponseDto
from application.handler.test_type_handler_interface import TestTypeHandlerInterface
from application.mapper.test_type_mapper import TestTypeMapper
from domain.api.test_type_service_port import TestTypeServicePort


class TestTypeHandler(TestTypeHandlerInterface):
    def __init__(
        self,
        test_type_mapper: TestTypeMapper,
        test_type_service_port: TestTypeServicePort,
    ):
        self.test_type_mapper = test_type_mapper
        self.test_type_service_port = test_type_service_port

    async def create_test_type(
        self, request: TestTypeRequestDto
    ) -> TestTypeResponseDto:
        test_type = self.test_type_mapper.to_test_type(request)
        created = await self.test_type_service_port.create_test_type(test_type)
        return self.test_type_mapper.to_response(created)

    async def get_test_types(self) -> list[TestTypeResponseDto]:
        test_types = await self.test_type_service_port.get_test_types()
        return self.test_type_mapper.to_response_list(test_types)

    async def get_test_type_by_id(
        self, request: GetTestTypeByIdRequestDto
    ) -> TestTypeResponseDto:
        test_type_id = self.test_type_mapper.to_test_type_id(request)
        test_type = await self.test_type_service_port.get_test_type_by_id(test_type_id)
        return self.test_type_mapper.to_response(test_type)

    async def update_test_type(
        self, request: UpdateTestTypeRequestDto
    ) -> TestTypeResponseDto:
        test_type = self.test_type_mapper.to_test_type(request.test_type)
        updated = await self.test_type_service_port.update_test_type(
            request.test_type_id, test_type
        )
        return self.test_type_mapper.to_response(updated)

    async def delete_test_type(self, request: DeleteTestTypeRequestDto) -> None:
        await self.test_type_service_port.delete_test_type(request.test_type_id)
