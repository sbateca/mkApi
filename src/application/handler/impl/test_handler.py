from application.dto.request import (
    DeleteTestRequestDto,
    GetTestByIdRequestDto,
    TestRequestDto,
    UpdateTestRequestDto,
)
from application.dto.response import TestResponseDto
from application.handler.test_handler_interface import TestHandlerInterface
from application.mapper.test_mapper import TestMapper
from domain.api.test_service_port import TestServicePort


class TestHandler(TestHandlerInterface):
    def __init__(self, mapper: TestMapper, service: TestServicePort):
        self.mapper = mapper
        self.service = service

    async def create_test(self, request: TestRequestDto) -> TestResponseDto:
        created = await self.service.create_test(self.mapper.to_test(request))
        return self.mapper.to_response(created)

    async def get_tests(self) -> list[TestResponseDto]:
        return self.mapper.to_response_list(await self.service.get_tests())

    async def get_test_by_id(self, request: GetTestByIdRequestDto) -> TestResponseDto:
        test = await self.service.get_test_by_id(self.mapper.to_test_id(request))
        return self.mapper.to_response(test)

    async def update_test(self, request: UpdateTestRequestDto) -> TestResponseDto:
        updated = await self.service.update_test(
            request.test_id,
            self.mapper.to_test(request.test),
        )
        return self.mapper.to_response(updated)

    async def delete_test(self, request: DeleteTestRequestDto) -> None:
        await self.service.delete_test(request.test_id)
