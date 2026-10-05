from application.dto.request.login_request_dto import LoginRequestDto
from application.dto.response.login_response_dto import LoginResponseDto
from domain.model.auth_tokens import AuthTokens
from domain.model.login_data import LoginData


class LoginMapper:
    def to_domain(self, login_request_dto: LoginRequestDto) -> LoginData:
        return LoginData(
            username=login_request_dto.username, password=login_request_dto.password
        )

    def to_response(self, tokens: AuthTokens) -> LoginResponseDto:
        return LoginResponseDto(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        )
