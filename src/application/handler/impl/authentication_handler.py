from application.dto.request.login_request_dto import LoginRequestDto
from application.dto.request.refresh_token_request_dto import RefreshTokenRequestDto
from application.dto.response.login_response_dto import LoginResponseDto
from application.handler.authentication_handler_interface import (
    AuthenticationHandlerInterface,
)
from application.mapper.login_mapper import LoginMapper
from domain.spi.authentication_service_port import AuthenticationServicePort


class AuthenticationHandler(AuthenticationHandlerInterface):
    def __init__(
        self,
        login_mapper: LoginMapper,
        authentication_service: AuthenticationServicePort,
    ):
        self.login_mapper = login_mapper
        self.authentication_service = authentication_service

    async def login(self, request_dto: LoginRequestDto) -> LoginResponseDto:
        login_data = self.login_mapper.to_domain(request_dto)
        tokens = await self.authentication_service.login(login_data)
        return self.login_mapper.to_response(tokens)

    async def refresh(self, request_dto: RefreshTokenRequestDto) -> LoginResponseDto:
        tokens = await self.authentication_service.refresh(request_dto.refresh_token)
        return self.login_mapper.to_response(tokens)

    async def logout(self, request_dto: RefreshTokenRequestDto) -> None:
        await self.authentication_service.logout(request_dto.refresh_token)
