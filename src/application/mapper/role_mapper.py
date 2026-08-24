from application.dto.request.role_request_dto import RoleRequestDto
from application.dto.response.role_response_dto import RoleResponseDto
from domain.model.role import Role


class RoleMapper:
    def to_domain(self, request: RoleRequestDto) -> Role:
        return Role(name=request.name)

    def to_response(self, role: Role) -> RoleResponseDto:
        return RoleResponseDto(id=role.id, name=role.name)

    def to_response_list(self, roles: list[Role]) -> list[RoleResponseDto]:
        return [self.to_response(role) for role in roles]
