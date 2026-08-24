from uuid import UUID

from application.dto.request.role_request_dto import RoleRequestDto
from application.dto.request.user_request_dto import UserRequestDto
from application.mapper.role_mapper import RoleMapper
from application.mapper.user_mapper import UserMapper
from domain.model.role import Role
from domain.model.user import User
from domain.util.constants import UserRole

ROLE_ID = UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5")
USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


def test_role_mapper_maps_requests_responses_and_lists():
    mapper = RoleMapper()
    role = Role(id=ROLE_ID, name=UserRole.ADMIN)

    assert mapper.to_domain(RoleRequestDto(name=UserRole.ADMIN)) == Role(
        name=UserRole.ADMIN
    )
    assert mapper.to_response(role).model_dump() == {
        "id": ROLE_ID,
        "name": UserRole.ADMIN,
    }
    assert mapper.to_response_list([role]) == [mapper.to_response(role)]


def test_user_mapper_maps_requests_responses_and_lists_without_password_output():
    mapper = UserMapper()
    request = UserRequestDto(
        name="Admin user",
        username="admin",
        password="password-123",
        email="admin@example.com",
        roles=[UserRole.ADMIN],
    )

    domain = mapper.to_domain(request)
    assert domain.roles == [Role(name=UserRole.ADMIN)]
    user = User(
        id=USER_ID,
        name=domain.name,
        username=domain.username,
        password="hashed-password",
        email=domain.email,
        roles=[Role(id=ROLE_ID, name=UserRole.ADMIN)],
    )
    response = mapper.to_response(user)

    assert response.id == USER_ID
    assert response.roles[0].id == ROLE_ID
    assert "password" not in response.model_dump()
    assert mapper.to_response_list([user]) == [response]
