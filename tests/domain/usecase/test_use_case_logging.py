from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from domain.exception.analysis_method_exception import AnalysisMethodNotFoundError
from domain.exception.analyte_exception import AnalyteNotFoundError
from domain.exception.client_exception import ClientNotFoundError
from domain.exception.sample_type_exception import SampleTypeNotFoundError
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from domain.spi.logger_port import LoggerPort
from domain.usecase.analysis_method_use_case import AnalysisMethodUseCase
from domain.usecase.analyte_use_case import AnalyteUseCase
from domain.usecase.client_use_case import ClientUseCase
from domain.usecase.sample_type_use_case import SampleTypeUseCase
from domain.usecase.test_type_use_case import TestTypeUseCase as TypeCatalogService
from tests.builders import ClientBuilder

RESOURCE_ID = "08dfffe2-c197-4726-b6ab-1e253c8e5f46"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "use_case_class",
        "port_method",
        "use_case_method",
        "start_message",
        "success_message",
    ),
    [
        (
            AnalysisMethodUseCase,
            "get_analysis_methods",
            "get_analysis_methods",
            "Retrieving analysis methods",
            "Analysis methods retrieved",
        ),
        (
            TypeCatalogService,
            "get_test_types",
            "get_test_types",
            "Retrieving test types",
            "Test types retrieved",
        ),
        (
            SampleTypeUseCase,
            "get_sample_types",
            "get_sample_types",
            "Retrieving sample types",
            "Sample types retrieved",
        ),
    ],
)
async def test_catalog_use_cases_log_list_success(
    use_case_class, port_method, use_case_method, start_message, success_message
):
    port = AsyncMock()
    getattr(port, port_method).return_value = []
    logger = MagicMock(spec=LoggerPort)
    use_case = use_case_class(port, logger)

    assert await getattr(use_case, use_case_method)() == []

    logger.info.assert_any_call(start_message)
    logger.info.assert_any_call(success_message, count=0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("use_case_class", "port_method", "use_case_method", "exception", "message"),
    [
        (
            AnalysisMethodUseCase,
            "get_analysis_method_by_id",
            "get_analysis_method_by_id",
            AnalysisMethodNotFoundError,
            "Analysis method not found",
        ),
        (
            TypeCatalogService,
            "get_test_type_by_id",
            "get_test_type_by_id",
            MissingTestTypeError,
            "Test type not found",
        ),
        (
            SampleTypeUseCase,
            "get_sample_type_by_id",
            "get_sample_type_by_id",
            SampleTypeNotFoundError,
            "Sample type not found",
        ),
    ],
)
async def test_catalog_use_cases_log_not_found(
    use_case_class, port_method, use_case_method, exception, message
):
    port = AsyncMock()
    getattr(port, port_method).return_value = None
    logger = MagicMock(spec=LoggerPort)
    use_case = use_case_class(port, logger)

    with pytest.raises(exception):
        await getattr(use_case, use_case_method)(RESOURCE_ID)

    logger.warning.assert_called_once()
    assert logger.warning.call_args.args[0] == message


@pytest.mark.asyncio
async def test_analyte_use_case_logs_success_and_not_found():
    analyte_port = AsyncMock()
    test_type_port = AsyncMock()
    logger = MagicMock(spec=LoggerPort)
    use_case = AnalyteUseCase(analyte_port, test_type_port, logger)
    analyte_port.get_analytes.return_value = []

    assert await use_case.get_analytes() == []
    logger.info.assert_any_call("Retrieving analytes")
    logger.info.assert_any_call("Analytes retrieved", count=0)

    analyte_port.get_analyte_by_id.return_value = None
    with pytest.raises(AnalyteNotFoundError):
        await use_case.get_analyte_by_id(RESOURCE_ID)
    logger.warning.assert_called_once_with("Analyte not found", analyte_id=RESOURCE_ID)


@pytest.mark.asyncio
async def test_client_use_case_logs_safe_create_metadata_and_not_found():
    persistence_port = AsyncMock()
    logger = MagicMock(spec=LoggerPort)
    use_case = ClientUseCase(persistence_port, logger)
    client = ClientBuilder().with_id(UUID(RESOURCE_ID)).build()
    persistence_port.get_client_by_email_or_nit.return_value = None
    persistence_port.save_client.return_value = client

    await use_case.create_client(client)

    logger.info.assert_any_call("Creating client", client_name=client.name)
    logger.info.assert_any_call("Client created", client_id=RESOURCE_ID)
    assert client.email not in str(logger.info.call_args_list)

    persistence_port.get_client_by_id.return_value = None
    with pytest.raises(ClientNotFoundError):
        await use_case.get_client_by_id(RESOURCE_ID)
    logger.warning.assert_called_once_with("Client not found", client_id=RESOURCE_ID)
