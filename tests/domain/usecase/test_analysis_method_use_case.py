from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from domain.exception.analysis_method_exception import (
    AnalysisMethodAlreadyExistsError,
    AnalysisMethodNotFoundError,
)
from domain.model.analysis_method import AnalysisMethod
from domain.spi.logger_port import LoggerPort
from domain.usecase.analysis_method_use_case import AnalysisMethodUseCase

ANALYSIS_METHOD_ID = UUID("c461270c-6682-4f51-9148-efb9fbaab44e")


@pytest.mark.asyncio
async def test_create_analysis_method_assigns_id_and_saves():
    analysis_method = AnalysisMethod(name="NTC")
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_name.return_value = None
    persistence_port.save_analysis_method.return_value = analysis_method
    use_case = AnalysisMethodUseCase(persistence_port)

    result = await use_case.create_analysis_method(analysis_method)

    assert result == analysis_method
    assert analysis_method.id is not None
    persistence_port.get_analysis_method_by_name.assert_awaited_once_with("NTC")
    persistence_port.save_analysis_method.assert_awaited_once_with(analysis_method)


@pytest.mark.asyncio
async def test_create_analysis_method_rejects_duplicate_name():
    analysis_method = AnalysisMethod(name="NTC")
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_name.return_value = AnalysisMethod(
        id=ANALYSIS_METHOD_ID, name="NTC"
    )
    use_case = AnalysisMethodUseCase(persistence_port)

    with pytest.raises(AnalysisMethodAlreadyExistsError):
        await use_case.create_analysis_method(analysis_method)

    persistence_port.save_analysis_method.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_analysis_method_by_id_rejects_missing_method():
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_id.return_value = None
    use_case = AnalysisMethodUseCase(persistence_port)

    with pytest.raises(AnalysisMethodNotFoundError):
        await use_case.get_analysis_method_by_id(str(ANALYSIS_METHOD_ID))


@pytest.mark.asyncio
async def test_get_analysis_method_by_id_returns_method_and_logs_success():
    stored = AnalysisMethod(id=ANALYSIS_METHOD_ID, name="NTC")
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_id.return_value = stored
    logger = MagicMock(spec=LoggerPort)
    use_case = AnalysisMethodUseCase(persistence_port, logger)

    assert await use_case.get_analysis_method_by_id(str(ANALYSIS_METHOD_ID)) == stored
    logger.info.assert_any_call(
        "Analysis method retrieved", analysis_method_id=str(ANALYSIS_METHOD_ID)
    )


@pytest.mark.asyncio
async def test_update_analysis_method_changes_name():
    current = AnalysisMethod(id=ANALYSIS_METHOD_ID, name="Old")
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_id.return_value = current
    persistence_port.get_analysis_method_by_name_excluding_id.return_value = None
    persistence_port.update_analysis_method.return_value = current
    use_case = AnalysisMethodUseCase(persistence_port)

    result = await use_case.update_analysis_method(
        str(ANALYSIS_METHOD_ID), AnalysisMethod(name="NTC")
    )

    assert result.name == "NTC"
    persistence_port.update_analysis_method.assert_awaited_once_with(current)


@pytest.mark.asyncio
async def test_update_analysis_method_rejects_duplicate_name_and_logs_warning():
    current = AnalysisMethod(id=ANALYSIS_METHOD_ID, name="Old")
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_id.return_value = current
    persistence_port.get_analysis_method_by_name_excluding_id.return_value = (
        AnalysisMethod(name="NTC")
    )
    logger = MagicMock(spec=LoggerPort)
    use_case = AnalysisMethodUseCase(persistence_port, logger)

    with pytest.raises(AnalysisMethodAlreadyExistsError):
        await use_case.update_analysis_method(
            str(ANALYSIS_METHOD_ID), AnalysisMethod(name="NTC")
        )

    logger.warning.assert_called_once_with(
        "Analysis method already exists",
        analysis_method_id=str(ANALYSIS_METHOD_ID),
    )
    persistence_port.update_analysis_method.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_analysis_method_requires_existing_method():
    stored = AnalysisMethod(id=ANALYSIS_METHOD_ID, name="NTC")
    persistence_port = AsyncMock()
    persistence_port.get_analysis_method_by_id.return_value = stored
    use_case = AnalysisMethodUseCase(persistence_port)

    await use_case.delete_analysis_method(str(ANALYSIS_METHOD_ID))

    persistence_port.delete_analysis_method.assert_awaited_once_with(ANALYSIS_METHOD_ID)
