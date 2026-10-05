from abc import ABC, abstractmethod

from application.dto.request.login_request_dto import LoginRequestDto
from application.dto.request.refresh_token_request_dto import RefreshTokenRequestDto
from application.dto.response.login_response_dto import LoginResponseDto


class AuthenticationHandlerInterface(ABC):
    @abstractmethod
    async def login(self, login_request_dto: LoginRequestDto) -> LoginResponseDto:
        pass

    @abstractmethod
    async def refresh(self, request_dto: RefreshTokenRequestDto) -> LoginResponseDto:
        pass

    @abstractmethod
    async def logout(self, request_dto: RefreshTokenRequestDto) -> None:
        pass
