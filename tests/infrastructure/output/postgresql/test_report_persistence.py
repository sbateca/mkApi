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
    retained, removed = uuid4(), uuid4()
    new_test = build_test_entity()
    retained_test = build_test_entity()
    retained_test.id = retained
    retained_test.result = "Edited result"
    updated, old_links, retained_row, saved_test, inserted, deleted, written_links = [
        Mock() for _ in range(7)
    ]
    updated.scalar_one_or_none.return_value = item.id
    old_links.scalars.return_value = [removed, retained]
    retained_row.one.return_value = (item.sample_id, False)
    inserted.scalars.return_value = [new_test.id]
    session.execute.side_effect = [
        updated,
        old_links,
        retained_row,
        saved_test,
        inserted,
        deleted,
        written_links,
    ]

    await repository.update_report(item, [retained_test, new_test])
    calls = session.execute.await_args_list
    assert "status" not in calls[0].args[0].compile().params
    assert calls[1].args[0].table.name == "report_tests"
    assert calls[3].args[0].compile().params["result"] == retained_test.result
    assert calls[4].args[0].table.name == "tests"
    assert calls[4].args[1][0]["id"] == new_test.id
    cleanup = calls[5].args[0].compile()
    assert "NOT (EXISTS" in str(cleanup)
    assert [removed] in cleanup.params.values()
    assert calls[6].args[1] == [
        {"report_id": item.id, "test_id": test_id, "position": position}
        for position, test_id in enumerate([retained, new_test.id])
    ]
    session.commit.assert_awaited_once()

    session.reset_mock()
    session.execute.side_effect = [
        updated,
        old_links,
        retained_row,
        saved_test,
        inserted,
        deleted,
        RuntimeError("link failure"),
    ]
    with pytest.raises(RuntimeError, match="link failure"):
        await repository.update_report(item, [retained_test, new_test])
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()


@pytest.mark.parametrize("fails", [False, True])
async def test_report_save_writes_ordered_links_after_flush(fails):
    from infrastructure.output.postgresql.adapter.report_test_persistence_adapter import (
        ReportTestPersistenceAdapter,
    )

    session = AsyncMock()
    session.add = Mock()
    repository = ReportPostgreSQLRepository(session)
    item = ReportEntity(id=uuid4())
    repository.get_report_by_id = AsyncMock(return_value=item)
    links = ReportTestPersistenceAdapter(session)
    tests = [build_test_entity(), build_test_entity()]
    tests[1].id = uuid4()
    ids = [test.id for test in tests]
    inserted = Mock()
    inserted.scalars.return_value = ids

    if fails:
        session.execute.side_effect = [inserted, RuntimeError("link insert failed")]
        with pytest.raises(RuntimeError, match="link insert failed"):
            await repository.save_report(item, tests, report_tests_port=links)
        assert [call[0] for call in session.mock_calls] == [
            "add",
            "flush",
            "execute",
            "execute",
            "rollback",
        ]
        repository.get_report_by_id.assert_not_awaited()
    else:
        session.execute.side_effect = [inserted, Mock()]
        assert (
            await repository.save_report(item, tests, report_tests_port=links) is item
        )
        assert [call[0] for call in session.mock_calls] == [
            "add",
            "flush",
            "execute",
            "execute",
            "commit",
        ]
        repository.get_report_by_id.assert_awaited_once_with(str(item.id))

    statement, rows = session.execute.await_args.args
    assert statement.table.name == "report_tests"
    assert rows == [
        {"report_id": item.id, "test_id": test_id, "position": position}
        for position, test_id in enumerate(ids)
    ]


@pytest.mark.parametrize("operation", ["edit", "delete", "approve"])
async def test_report_mutations_reject_concurrent_status_change(operation):
    from domain.exception.report_exception import ReportActionDeniedError

    session = AsyncMock()
    repository = ReportPostgreSQLRepository(session)
    report_id = uuid4()
    skipped_write, existing_report = Mock(), Mock()
    skipped_write.scalar_one_or_none.return_value = None
    existing_report.scalar_one_or_none.return_value = report_id
    session.execute.side_effect = [skipped_write, existing_report]

    with pytest.raises(ReportActionDeniedError, match="report_not_draft"):
        if operation == "edit":
            await repository.update_report(ReportEntity(id=report_id), [])
        elif operation == "delete":
            await repository.delete_report(str(report_id))
        else:
            await repository.update_report_status(str(report_id), "Approved")

    statement = session.execute.await_args_list[0].args[0].compile()
    assert "lower(reports.status)" in str(statement)
    assert "draft" in statement.params.values()
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()


async def test_report_delete_removes_owned_tests_in_the_same_transaction():
    session = AsyncMock()
    repository = ReportPostgreSQLRepository(session)
    report_id, test_id = uuid4(), uuid4()
    locked, links = Mock(), Mock()
    locked.scalar_one_or_none.return_value = report_id
    links.scalars.return_value = [test_id]
    session.execute.side_effect = [locked, links, Mock(), Mock()]

    await repository.delete_report(str(report_id))

    calls = session.execute.await_args_list
    assert "FOR UPDATE" in str(calls[0].args[0].compile())
    assert [call.args[0].table.name for call in calls[1:]] == [
        "report_tests",
        "tests",
        "reports",
    ]
    assert [test_id] in calls[2].args[0].compile().params.values()
    session.commit.assert_awaited_once()


async def test_report_save_rejects_test_id_already_used():
    from domain.exception.domain_exception import DomainError
    from domain.util.constants import REPORT_TEST_ID_ALREADY_EXISTS_ERROR_MESSAGE

    session = AsyncMock()
    session.add = Mock()
    repository = ReportPostgreSQLRepository(session)
    inserted = Mock()
    inserted.scalars.return_value = []
    session.execute.return_value = inserted

    with pytest.raises(DomainError, match=REPORT_TEST_ID_ALREADY_EXISTS_ERROR_MESSAGE):
        await repository.save_report(ReportEntity(id=uuid4()), [build_test_entity()])

    session.execute.assert_awaited_once()
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()


async def test_report_approval_locks_sample_before_changing_status():
    from sqlalchemy.dialects import postgresql

    session = AsyncMock()
    repository = ReportPostgreSQLRepository(session)
    report_id = uuid4()
    sample_id = domain_sample().id
    locked_report = Mock()
    locked_report.scalar_one_or_none.return_value = sample_id
    session.execute.side_effect = [locked_report, Mock(), Mock()]
    repository.get_report_by_id = AsyncMock(return_value=ReportEntity(id=report_id))

    await repository.update_report_status(str(report_id), "Approved")

    report_lock, sample_lock, write = [
        call.args[0].compile(dialect=postgresql.dialect())
        for call in session.execute.await_args_list
    ]
    assert "FOR UPDATE" in str(report_lock)
    assert "FOR NO KEY UPDATE" in str(sample_lock)
    assert sample_id in sample_lock.params.values()
    assert write.params["status"] == "Approved"
    session.commit.assert_awaited_once()


async def test_report_write_conflict_rolls_back_if_sample_already_has_report():
    from asyncpg.exceptions import UniqueViolationError
    from sqlalchemy.exc import IntegrityError

    from domain.exception.report_exception import ReportAlreadyExistsError
    from infrastructure.output.postgresql.entity.report_entity import (
        REPORT_SAMPLE_INDEX,
    )

    session = AsyncMock()
    session.add = Mock()
    violation = UniqueViolationError()
    violation.constraint_name = REPORT_SAMPLE_INDEX
    driver_error = RuntimeError()
    driver_error.__cause__ = violation
    session.flush.side_effect = IntegrityError(None, None, driver_error)
    repository = ReportPostgreSQLRepository(session)

    with pytest.raises(ReportAlreadyExistsError):
        await repository.save_report(ReportEntity(id=uuid4()), [])

    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()
