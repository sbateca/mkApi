from uuid import UUID

from domain.model.role import Role
from domain.model.user import User
from domain.util.constants import UserRole
from infrastructure.output.postgresql.entity.role_entity import RoleEntity
from infrastructure.output.postgresql.entity.user_entity import UserEntity
from infrastructure.output.postgresql.entity.user_role_entity import UserRoleEntity
from infrastructure.output.postgresql.mapper.role_entity_mapper import RoleEntityMapper
from infrastructure.output.postgresql.mapper.user_entity_mapper import UserEntityMapper

ROLE_ID = UUID("300f99a7-620e-4cc1-9c52-7848098bc6e5")
USER_ID = UUID("a43b10d8-3ba7-4e2a-a510-baf8ac45dc1e")


def test_role_entity_mapper_maps_both_directions_and_lists():
    mapper = RoleEntityMapper()
    domain = Role(id=ROLE_ID, name=UserRole.ADMIN)
    entity = mapper.to_entity(domain)

    assert entity.id == ROLE_ID
    assert entity.name == "Admin"
    assert mapper.to_domain(entity) == domain
    assert mapper.to_domain_list([entity]) == [domain]


def test_user_entity_mapper_maps_roles_both_directions():
    role_mapper = RoleEntityMapper()
    mapper = UserEntityMapper(role_mapper)
    domain = User(
        id=USER_ID,
        name="Admin user",
        username="admin",
        password="hashed-password",
        email="admin@example.com",
        roles=[Role(id=ROLE_ID, name=UserRole.ADMIN)],
    )

    entity = mapper.to_entity(domain)
    assert entity.user_roles[0].role_id == ROLE_ID

    loaded_role = RoleEntity(id=ROLE_ID, name="Admin")
    loaded_join = UserRoleEntity(user_id=USER_ID, role_id=ROLE_ID)
    loaded_join.role = loaded_role
    loaded_user = UserEntity(
        id=USER_ID,
        name=domain.name,
        username=domain.username,
        password=domain.password,
        email=domain.email,
    )
    loaded_user.user_roles = [loaded_join]

    assert mapper.to_domain(loaded_user) == domain
