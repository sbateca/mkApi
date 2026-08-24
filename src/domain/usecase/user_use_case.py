from uuid import UUID, uuid4

from domain.api.user_service_port import UserServicePort
from domain.exception.user_exception import UserAlreadyExistsError, UserNotFoundError
from domain.model.user import User
from domain.spi.logger_port import LoggerPort, NullLogger
from domain.spi.password_hasher_port import PasswordHasherPort
from domain.spi.user_persistence_port import UserPersistencePort
from src.domain.spi.role_persistence_port import RolePersistencePort


class UserUseCase(UserServicePort):
    def __init__(
        self,
        user_persistence_port: UserPersistencePort,
        role_persistence_port: RolePersistencePort,
        password_hasher: PasswordHasherPort,
        logger: LoggerPort | None = None,
    ):
        self.user_persistence_port = user_persistence_port
        self.role_persistence_port = role_persistence_port
        self.password_hasher = password_hasher
        self.logger = logger or NullLogger()

    async def create_user(self, user: User) -> User:
        self.logger.info("Creating user", username=user.username)

        await self.__validate_unique_user(user.email, user.username)
        roles = await self.role_persistence_port.find_roles_by_names(
            [role.name.value for role in user.roles]
        )
        user.roles = roles
        user.password = self.password_hasher.hash(user.password)
        if not user.id:
            user.id = uuid4()

        return await self.user_persistence_port.save(user)

    async def get_users(self) -> list[User]:
        if self.logger:
            self.logger.info("Fetching all users")
        return await self.user_persistence_port.find_all()

    async def get_user_by_id(self, user_id: str) -> User:
        self.logger.info("Fetching user by ID", user_id=user_id)
        return await self.__request_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        if self.logger:
            self.logger.info(f"Fetching user by email: {email}")
        return await self.user_persistence_port.find_by_email(email)

    async def update_user(self, user_id: str, updated_user: User) -> User:
        self.logger.info("Updating user", user_id=user_id)
        current = await self.__request_user_by_id(user_id)
        await self.__validate_unique_user(
            updated_user.email,
            updated_user.username,
            current.id,
        )

        updated_user.id = current.id
        updated_user.password = self.password_hasher.hash(updated_user.password)
        roles = await self.role_persistence_port.find_roles_by_names(
            [role.name.value for role in updated_user.roles]
        )
        updated_user.roles = roles
        return await self.user_persistence_port.update(user_id, updated_user)

    async def delete_user(self, user_id: str) -> None:
        await self.__request_user_by_id(user_id)
        self.logger.info("Deleting user", user_id=user_id)
        await self.user_persistence_port.delete(user_id)

    async def __request_user_by_id(self, user_id: str) -> User:
        user = await self.user_persistence_port.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def __validate_unique_user(
        self,
        email: str,
        username: str,
        current_user_id: UUID | None = None,
    ) -> None:
        user_with_email = await self.user_persistence_port.find_by_email(email)
        if user_with_email and user_with_email.id != current_user_id:
            raise UserAlreadyExistsError()
        user_with_username = await self.user_persistence_port.find_by_username(username)
        if user_with_username and user_with_username.id != current_user_id:
            raise UserAlreadyExistsError()
