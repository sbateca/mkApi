from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.handler.analysis_method_handler_interface import (
    AnalysisMethodHandlerInterface,
)
from application.handler.analyte_handler_interface import AnalyteHandlerInterface
from application.handler.client_handler_interface import ClientHandlerInterface
from application.handler.criteria_handler_interface import CriteriaHandlerInterface
from application.handler.impl.analysis_method_handler import AnalysisMethodHandler
from application.handler.impl.analyte_handler import AnalyteHandler
from application.handler.impl.client_handler import ClientHandler
from application.handler.impl.criteria_handler import CriteriaHandler
from application.handler.impl.sample_handler import SampleHandler
from application.handler.impl.sample_type_handler import SampleTypeHandler
from application.handler.impl.test_type_handler import TestTypeHandler
from application.handler.sample_handler_interface import SampleHandlerInterface
from application.handler.sample_type_handler_interface import SampleTypeHandlerInterface
from application.handler.test_type_handler_interface import TestTypeHandlerInterface
from application.mapper.analysis_method_mapper import AnalysisMethodMapper
from application.mapper.analyte_mapper import AnalyteMapper
from application.mapper.client_mapper import ClientMapper
from application.mapper.criteria_mapper import CriteriaMapper
from application.mapper.sample_mapper import SampleMapper
from application.mapper.sample_type_mapper import SampleTypeMapper
from application.mapper.test_type_mapper import TestTypeMapper
from domain.api.analysis_method_service_port import AnalysisMethodServicePort
from domain.api.analyte_service_port import AnalyteServicePort
from domain.api.client_service_port import ClientServicePort
from domain.api.criteria_service_port import CriteriaServicePort
from domain.api.sample_service_port import SampleServicePort
from domain.api.sample_type_service_port import SampleTypeServicePort
from domain.api.test_type_service_port import TestTypeServicePort
from domain.spi.analysis_method_persistence_port import AnalysisMethodPersistencePort
from domain.spi.analyte_persistence_port import AnalytePersistencePort
from domain.spi.client_persistence_port import ClientPersistencePort
from domain.spi.criteria_persistence_port import CriteriaPersistencePort
from domain.spi.sample_persistence_port import SamplePersistencePort
from domain.spi.sample_type_persistence_port import SampleTypePersistencePort
from domain.spi.test_type_persistence_port import TestTypePersistencePort
from domain.usecase.analysis_method_use_case import AnalysisMethodUseCase
from domain.usecase.analyte_use_case import AnalyteUseCase
from domain.usecase.client_use_case import ClientUseCase
from domain.usecase.criteria_use_case import CriteriaUseCase
from domain.usecase.sample_type_use_case import SampleTypeUseCase
from domain.usecase.sample_use_case import SampleUseCase
from domain.usecase.test_type_use_case import TestTypeUseCase
from infrastructure.output.observability.logger_adapter import (
    LoggerAdapter,
)
from infrastructure.output.postgresql.adapter.analysis_method_persistence_adapter import (
    AnalysisMethodPersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.analyte_persistence_adapter import (
    AnalytePersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.client_persistence_adapter import (
    ClientPersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.criteria_persistence_adapter import (
    CriteriaPersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.sample_persistence_adapter import (
    SamplePersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.sample_type_persistence_adapter import (
    SampleTypePersistenceAdapter,
)
from infrastructure.output.postgresql.adapter.test_type_persistence_adapter import (
    TestTypePersistenceAdapter,
)
from infrastructure.output.postgresql.database.session import get_db_session
from infrastructure.output.postgresql.mapper.analysis_method_entity_mapper import (
    AnalysisMethodEntityMapper,
)
from infrastructure.output.postgresql.mapper.analyte_entity_mapper import (
    AnalyteEntityMapper,
)
from infrastructure.output.postgresql.mapper.client_entity_mapper import (
    ClientEntityMapper,
)
from infrastructure.output.postgresql.mapper.criteria_entity_mapper import (
    CriteriaEntityMapper,
)
from infrastructure.output.postgresql.mapper.sample_entity_mapper import (
    SampleEntityMapper,
)
from infrastructure.output.postgresql.mapper.sample_type_entity_mapper import (
    SampleTypeEntityMapper,
)
from infrastructure.output.postgresql.mapper.test_type_entity_mapper import (
    TestTypeEntityMapper,
)
from infrastructure.output.postgresql.repository.analysis_method_repository import (
    AnalysisMethodPostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.analyte_repository import (
    AnalytePostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.client_repository import (
    ClientPostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.criteria_repository import (
    CriteriaPostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.sample_repository import (
    SamplePostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.sample_type_repository import (
    SampleTypePostgreSQLRepository,
)
from infrastructure.output.postgresql.repository.test_type_repository import (
    TestTypePostgreSQLRepository,
)


def get_criteria_mapper() -> CriteriaMapper:
    return CriteriaMapper()


def get_criteria_entity_mapper() -> CriteriaEntityMapper:
    return CriteriaEntityMapper()


def get_criteria_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CriteriaPostgreSQLRepository:
    return CriteriaPostgreSQLRepository(session)


def get_criteria_persistence_adapter(
    repository: Annotated[
        CriteriaPostgreSQLRepository, Depends(get_criteria_repository)
    ],
    entity_mapper: Annotated[CriteriaEntityMapper, Depends(get_criteria_entity_mapper)],
) -> CriteriaPersistencePort:
    return CriteriaPersistenceAdapter(repository, entity_mapper)


def get_criteria_usecase(
    persistence_port: Annotated[
        CriteriaPersistencePort, Depends(get_criteria_persistence_adapter)
    ],
) -> CriteriaServicePort:
    return CriteriaUseCase(persistence_port, LoggerAdapter("mkapi.criteria"))


def get_criteria_handler(
    mapper: Annotated[CriteriaMapper, Depends(get_criteria_mapper)],
    service: Annotated[CriteriaServicePort, Depends(get_criteria_usecase)],
) -> CriteriaHandlerInterface:
    return CriteriaHandler(mapper, service)


def get_sample_type_mapper() -> SampleTypeMapper:
    return SampleTypeMapper()


def get_sample_type_entity_mapper() -> SampleTypeEntityMapper:
    return SampleTypeEntityMapper()


def get_sample_type_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SampleTypePostgreSQLRepository:
    return SampleTypePostgreSQLRepository(session)


def get_sample_type_persistence_adapter(
    repository: Annotated[
        SampleTypePostgreSQLRepository, Depends(get_sample_type_repository)
    ],
    entity_mapper: Annotated[
        SampleTypeEntityMapper, Depends(get_sample_type_entity_mapper)
    ],
) -> SampleTypePersistencePort:
    return SampleTypePersistenceAdapter(repository, entity_mapper)


def get_sample_type_usecase(
    persistence_port: Annotated[
        SampleTypePersistencePort, Depends(get_sample_type_persistence_adapter)
    ],
) -> SampleTypeServicePort:
    return SampleTypeUseCase(persistence_port, LoggerAdapter("mkapi.sample_type"))


def get_sample_type_handler(
    mapper: Annotated[SampleTypeMapper, Depends(get_sample_type_mapper)],
    service: Annotated[SampleTypeServicePort, Depends(get_sample_type_usecase)],
) -> SampleTypeHandlerInterface:
    return SampleTypeHandler(mapper, service)


def get_test_type_mapper() -> TestTypeMapper:
    return TestTypeMapper()


def get_test_type_entity_mapper() -> TestTypeEntityMapper:
    return TestTypeEntityMapper()


def get_test_type_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TestTypePostgreSQLRepository:
    return TestTypePostgreSQLRepository(session)


def get_test_type_persistence_adapter(
    repository: Annotated[
        TestTypePostgreSQLRepository, Depends(get_test_type_repository)
    ],
    entity_mapper: Annotated[
        TestTypeEntityMapper, Depends(get_test_type_entity_mapper)
    ],
) -> TestTypePersistencePort:
    return TestTypePersistenceAdapter(repository, entity_mapper)


def get_test_type_usecase(
    persistence_port: Annotated[
        TestTypePersistencePort, Depends(get_test_type_persistence_adapter)
    ],
) -> TestTypeServicePort:
    return TestTypeUseCase(persistence_port, LoggerAdapter("mkapi.test_type"))


def get_test_type_handler(
    mapper: Annotated[TestTypeMapper, Depends(get_test_type_mapper)],
    service_port: Annotated[TestTypeServicePort, Depends(get_test_type_usecase)],
) -> TestTypeHandlerInterface:
    return TestTypeHandler(mapper, service_port)


def get_analyte_mapper() -> AnalyteMapper:
    return AnalyteMapper()


def get_analyte_entity_mapper(
    test_type_entity_mapper: Annotated[
        TestTypeEntityMapper, Depends(get_test_type_entity_mapper)
    ],
) -> AnalyteEntityMapper:
    return AnalyteEntityMapper(test_type_entity_mapper)


def get_analyte_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AnalytePostgreSQLRepository:
    return AnalytePostgreSQLRepository(session)


def get_analyte_persistence_adapter(
    repository: Annotated[AnalytePostgreSQLRepository, Depends(get_analyte_repository)],
    entity_mapper: Annotated[AnalyteEntityMapper, Depends(get_analyte_entity_mapper)],
) -> AnalytePersistencePort:
    return AnalytePersistenceAdapter(repository, entity_mapper)


def get_analyte_usecase(
    analyte_persistence_port: Annotated[
        AnalytePersistencePort, Depends(get_analyte_persistence_adapter)
    ],
    test_type_persistence_port: Annotated[
        TestTypePersistencePort, Depends(get_test_type_persistence_adapter)
    ],
) -> AnalyteServicePort:
    return AnalyteUseCase(
        analyte_persistence_port,
        test_type_persistence_port,
        LoggerAdapter("mkapi.analyte"),
    )


def get_analyte_handler(
    mapper: Annotated[AnalyteMapper, Depends(get_analyte_mapper)],
    service: Annotated[AnalyteServicePort, Depends(get_analyte_usecase)],
) -> AnalyteHandlerInterface:
    return AnalyteHandler(mapper, service)


def get_analysis_method_mapper() -> AnalysisMethodMapper:
    return AnalysisMethodMapper()


def get_analysis_method_entity_mapper() -> AnalysisMethodEntityMapper:
    return AnalysisMethodEntityMapper()


def get_analysis_method_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AnalysisMethodPostgreSQLRepository:
    return AnalysisMethodPostgreSQLRepository(session)


def get_analysis_method_persistence_adapter(
    repository: Annotated[
        AnalysisMethodPostgreSQLRepository,
        Depends(get_analysis_method_repository),
    ],
    entity_mapper: Annotated[
        AnalysisMethodEntityMapper,
        Depends(get_analysis_method_entity_mapper),
    ],
) -> AnalysisMethodPersistencePort:
    return AnalysisMethodPersistenceAdapter(repository, entity_mapper)


def get_analysis_method_usecase(
    persistence_port: Annotated[
        AnalysisMethodPersistencePort,
        Depends(get_analysis_method_persistence_adapter),
    ],
) -> AnalysisMethodServicePort:
    return AnalysisMethodUseCase(
        persistence_port, LoggerAdapter("mkapi.analysis_method")
    )


def get_analysis_method_handler(
    mapper: Annotated[AnalysisMethodMapper, Depends(get_analysis_method_mapper)],
    service_port: Annotated[
        AnalysisMethodServicePort,
        Depends(get_analysis_method_usecase),
    ],
) -> AnalysisMethodHandlerInterface:
    return AnalysisMethodHandler(mapper, service_port)


def get_client_mapper() -> ClientMapper:
    return ClientMapper()


def get_client_entity_mapper() -> ClientEntityMapper:
    return ClientEntityMapper()


def get_client_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ClientPostgreSQLRepository:
    return ClientPostgreSQLRepository(session)


def get_client_persistence_adapter(
    client_repository: Annotated[
        ClientPostgreSQLRepository,
        Depends(get_client_repository),
    ],
    client_entity_mapper: Annotated[
        ClientEntityMapper,
        Depends(get_client_entity_mapper),
    ],
) -> ClientPersistencePort:
    return ClientPersistenceAdapter(
        client_repository=client_repository,
        client_entity_mapper=client_entity_mapper,
    )


def get_client_usecase(
    client_persistence_port: Annotated[
        ClientPersistencePort,
        Depends(get_client_persistence_adapter),
    ],
) -> ClientServicePort:
    return ClientUseCase(
        client_persistence_port=client_persistence_port,
        logger=LoggerAdapter("mkapi.client"),
    )


def get_client_handler(
    client_mapper: Annotated[
        ClientMapper,
        Depends(get_client_mapper),
    ],
    client_service_port: Annotated[
        ClientServicePort,
        Depends(get_client_usecase),
    ],
) -> ClientHandlerInterface:
    return ClientHandler(
        client_mapper=client_mapper,
        client_service_port=client_service_port,
    )


def get_sample_mapper() -> SampleMapper:
    return SampleMapper()


def get_sample_entity_mapper(
    sample_type_entity_mapper: Annotated[
        SampleTypeEntityMapper, Depends(get_sample_type_entity_mapper)
    ],
    client_entity_mapper: Annotated[
        ClientEntityMapper, Depends(get_client_entity_mapper)
    ],
) -> SampleEntityMapper:
    return SampleEntityMapper(sample_type_entity_mapper, client_entity_mapper)


def get_sample_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SamplePostgreSQLRepository:
    return SamplePostgreSQLRepository(session)


def get_sample_persistence_adapter(
    repository: Annotated[SamplePostgreSQLRepository, Depends(get_sample_repository)],
    entity_mapper: Annotated[SampleEntityMapper, Depends(get_sample_entity_mapper)],
) -> SamplePersistencePort:
    return SamplePersistenceAdapter(repository, entity_mapper)


def get_sample_usecase(
    sample_persistence_port: Annotated[
        SamplePersistencePort, Depends(get_sample_persistence_adapter)
    ],
    sample_type_persistence_port: Annotated[
        SampleTypePersistencePort, Depends(get_sample_type_persistence_adapter)
    ],
    client_persistence_port: Annotated[
        ClientPersistencePort, Depends(get_client_persistence_adapter)
    ],
) -> SampleServicePort:
    return SampleUseCase(
        sample_persistence_port,
        sample_type_persistence_port,
        client_persistence_port,
        LoggerAdapter("mkapi.sample"),
    )


def get_sample_handler(
    mapper: Annotated[SampleMapper, Depends(get_sample_mapper)],
    service: Annotated[SampleServicePort, Depends(get_sample_usecase)],
) -> SampleHandlerInterface:
    return SampleHandler(mapper, service)
