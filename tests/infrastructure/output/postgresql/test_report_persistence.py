from datetime import date
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from infrastructure.output.postgresql.entity.report_entity import ReportEntity
from infrastructure.output.postgresql.mapper.report_entity_mapper import (
    ReportEntityMapper,
)
from infrastructure.output.postgresql.repository.report_repository import (
    ReportPostgreSQLRepository,
)
from tests.builders.report_builder import report
from tests.builders.report_sample_builder import (
    domain_sample,
    sample_entity,
    sample_mapper,
)
from tests.builders.report_test_builder import (
    build_test_entity,
    build_test_mapper,
)


def test_report_entity_mapper_nested_shape():
    item = report()
    mapper = ReportEntityMapper(sample_mapper(), build_test_mapper())
    entity = mapper.to_entity(item)
    entity.sample = sample_entity()
    entity.tests = [build_test_entity()]
    assert mapper.to_domain(entity) == item
    assert mapper.to_domain(None) is None


async def test_report_repository_replaces_links_atomically_and_rolls_back():
    session = AsyncMock()
    session.add = Mock()
    repository = ReportPostgreSQLRepository(session)
    repository.get_report_by_id = AsyncMock(return_value=ReportEntity(id=uuid4()))
    item = ReportEntity(
        id=uuid4(),
        sample_id=domain_sample().id,
        report_number="R",
        report_date=date.today(),
        status="draft",
    )
    ids = [uuid4(), uuid4()]
    await repository.update_report(item, ids)
    calls = session.execute.await_args_list
    assert calls[0].args[0].table.name == "report_tests"
    assert calls[1].args[1] == [
        {"report_id": item.id, "test_id": test_id, "position": i}
        for i, test_id in enumerate(ids)
    ]
    session.commit.assert_awaited_once()
    session.execute.side_effect = RuntimeError("database failure")
    with pytest.raises(RuntimeError):
        await repository.save_report(item, ids)
    session.rollback.assert_awaited_once()
