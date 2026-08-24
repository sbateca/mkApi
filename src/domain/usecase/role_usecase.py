from domain.api.role_service_port import RoleServicePort
from domain.exception.role_exception import RoleAlreadyExistsError, RoleNotFoundError
from domain.model.role import Role
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.role_persistence_port import RolePersistencePort


class RoleUseCase(RoleServicePort):
    def __init__(
        self,
        role_persistence_port: RolePersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.role_persistence_port = role_persistence_port
        self.logger = logger or NullLogger()

    async def create_role(self, role: Role) -> Role:
        await self.__validate_role_non_exists_by_name(role.name.value)

        self.logger.info("Creating role", name=role.name)
        created = await self.role_persistence_port.save(role)
        self.logger.info("Role created", role_name=str(created.name))
        return created

    async def get_roles(self) -> list[Role]:
        self.logger.info("Fetching all roles")
        return await self.role_persistence_port.find_all()

    async def get_role_by_id(self, role_id: str) -> Role:
        self.logger.info("Fetching role by ID", role_id=role_id)
        return await self.__request_role_by_id(role_id)

    async def get_role_by_name(self, name: str) -> Role | None:
        self.logger.info("Fetching role by name", role_name=name)
        return await self.role_persistence_port.find_by_name(name)

    async def find_roles_by_names(self, role_names: list[str]) -> list[Role]:
        self.logger.info("Fetching roles by names", role_names=role_names)
        return await self.role_persistence_port.find_roles_by_names(role_names)

    async def update_role(self, role_id: str, updated_role: Role) -> Role:
        self.logger.info("Updating role", role_id=role_id)
        current = await self.__request_role_by_id(role_id)
        same_name = await self.role_persistence_port.find_by_name(
            updated_role.name.value
        )
        if same_name and str(same_name.id) != str(current.id):
            raise RoleAlreadyExistsError()
        updated_role.id = current.id
        return await self.role_persistence_port.update(role_id, updated_role)

    async def delete_role(self, role_id: str) -> None:
        self.logger.info("Deleting role", role_id=role_id)
        await self.__request_role_by_id(role_id)
        await self.role_persistence_port.delete(role_id)

    async def __request_role_by_id(self, role_id: str) -> Role:
        role = await self.role_persistence_port.find_by_id(role_id)
        if not role:
            self.logger.error("Role not found", role_id=role_id)
            raise RoleNotFoundError()
        return role

    async def __validate_role_non_exists_by_name(self, name: str) -> None:
        role = await self.role_persistence_port.find_by_name(name)
        if role:
            self.logger.error("Role already exists", name=name)
            raise RoleAlreadyExistsError()

    async def __validate_roles_non_exists_by_names(self, role_names: list[str]) -> None:
        roles = await self.role_persistence_port.find_roles_by_names(role_names)
        if roles:
            existing_names = [role.name for role in roles]
            self.logger.error("Roles already exist", names=existing_names)
            raise RoleAlreadyExistsError(
                f"Roles already exist: {', '.join(existing_names)}"
            )
