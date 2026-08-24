from application.dto.request.user_request_dto import UserRequestDto
from application.dto.response.role_response_dto import RoleResponseDto
from application.dto.response.user_response_dto import UserResponseDto
from domain.model.role import Role
from domain.model.user import User


class UserMapper:
    def to_domain(self, request: UserRequestDto) -> User:
        return User(
            name=request.name,
            username=request.username,
            password=request.password,
            email=str(request.email),
            roles=[Role(name=name) for name in request.roles],
        )

    def to_response(self, user: User) -> UserResponseDto:
        return UserResponseDto(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            roles=[RoleResponseDto(id=role.id, name=role.name) for role in user.roles],
        )

    def to_response_list(self, users: list[User]) -> list[UserResponseDto]:
        return [self.to_response(user) for user in users]
