from uuid import uuid4

from domain.api.criteria_service_port import CriteriaServicePort
from domain.exception.criteria_exception import (
    CriteriaAlreadyExistsError,
    CriteriaNotFoundError,
)
from domain.model.criteria import Criteria
from domain.spi.criteria_persistence_port import CriteriaPersistencePort
from domain.spi.logger_port import LoggerPort, NullLogger


class CriteriaUseCase(CriteriaServicePort):
    def __init__(
        self,
        persistence_port: CriteriaPersistencePort,
        logger: LoggerPort | None = None,
    ):
        self.persistence_port = persistence_port
        self.logger = logger or NullLogger()

    async def create_criteria(self, criteria: Criteria) -> Criteria:
        self.logger.info("Creating criteria", name=criteria.name)
        await self.__validate_name_is_available(criteria.name)
        if not criteria.id:
            criteria.id = uuid4()
        created = await self.persistence_port.save_criteria(criteria)
        self.logger.info("Criteria created", criteria_id=str(created.id))
        return created

    async def get_criteria(self) -> list[Criteria]:
        self.logger.info("Retrieving criteria")
        criteria = await self.persistence_port.get_criteria()
        self.logger.info("Criteria retrieved", count=len(criteria))
        return criteria

    async def get_criteria_by_id(self, criteria_id: str) -> Criteria:
        self.logger.info("Retrieving criteria", criteria_id=criteria_id)
        criteria = await self.__request_criteria_by_id(criteria_id)
        self.logger.info("Criteria retrieved", criteria_id=str(criteria.id))
        return criteria

    async def update_criteria(
        self, criteria_id: str, updated_criteria: Criteria
    ) -> Criteria:
        self.logger.info("Updating criteria", criteria_id=criteria_id)
        current = await self.__request_criteria_by_id(criteria_id)
        duplicate = await self.persistence_port.get_criteria_by_name_excluding_id(
            updated_criteria.name, criteria_id
        )
        if duplicate:
            self.logger.warning("Criteria already exists", criteria_id=criteria_id)
            raise CriteriaAlreadyExistsError()

        current.name = updated_criteria.name
        updated = await self.persistence_port.update_criteria(current)
        self.logger.info("Criteria updated", criteria_id=str(updated.id))
        return updated

    async def delete_criteria(self, criteria_id: str) -> None:
        self.logger.info("Deleting criteria", criteria_id=criteria_id)
        criteria = await self.__request_criteria_by_id(criteria_id)
        await self.persistence_port.delete_criteria(criteria.id)
        self.logger.info("Criteria deleted", criteria_id=str(criteria.id))

    async def __validate_name_is_available(self, name: str) -> None:
        if await self.persistence_port.get_criteria_by_name(name):
            self.logger.warning("Criteria already exists")
            raise CriteriaAlreadyExistsError()

    async def __request_criteria_by_id(self, criteria_id: str) -> Criteria:
        criteria = await self.persistence_port.get_criteria_by_id(criteria_id)
        if criteria is None:
            self.logger.warning("Criteria not found", criteria_id=criteria_id)
            raise CriteriaNotFoundError()
        return criteria
