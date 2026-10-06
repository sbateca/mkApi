from uuid import uuid4

import pytest

from application.dto.request import ReportRequestDto
from application.mapper.report_mapper import ReportMapper
from domain.exception.report_exception import (
    ReportNotFoundError,
    ReportSampleConsistencyError,
)
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_exception import TestNotFoundError as MissingTestError
from tests.builders.report_builder import body, report, service
from tests.builders.report_sample_builder import (
    domain_sample,
)
from tests.builders.report_test_builder import domain_test


async def test_report_crud_resolves_relations_and_preserves_identity():
    usecase, persistence, _, _ = service()
    item = ReportMapper().to_report(ReportRequestDto(**body()))
    created = await usecase.create_report(item)
    assert created.id is not None
    assert created.sample == domain_sample()
    assert created.tests == [domain_test()]
    persistence.get_report_by_id.return_value = created
    persistence.get_reports.return_value = [created]
    assert await usecase.get_reports() == [created]
    changed = report()
    changed.report_number = "Updated"
    changed.tests = []
    updated = await usecase.update_report(str(created.id), changed)
    assert updated.id == created.id
    assert updated.tests == []
    await usecase.delete_report(str(created.id))
    persistence.delete_report.assert_awaited_once_with(str(created.id))


@pytest.mark.parametrize("missing", ["sample", "test", "mismatch"])
async def test_report_invalid_relations_do_not_write(missing):
    usecase, persistence, samples, tests = service()
    if missing == "sample":
        samples.get_sample_by_id.return_value = None
        error = SampleNotFoundError
    elif missing == "test":
        tests.get_test_by_id.return_value = None
        error = MissingTestError
    else:
        tests.get_test_by_id.return_value.sample_id = str(uuid4())
        error = ReportSampleConsistencyError
    with pytest.raises(error):
        await usecase.create_report(report())
    persistence.save_report.assert_not_awaited()


async def test_report_missing_blocks_read_update_delete():
    usecase, persistence, _, _ = service()
    persistence.get_report_by_id.return_value = None
    for operation in [
        usecase.get_report_by_id("missing"),
        usecase.update_report("missing", report()),
        usecase.delete_report("missing"),
    ]:
        with pytest.raises(ReportNotFoundError):
            await operation
    persistence.update_report.assert_not_awaited()
    persistence.delete_report.assert_not_awaited()


@pytest.mark.parametrize("operation", ["create", "update"])
async def test_report_duplicate_test_ids_do_not_write(operation):
    from domain.exception.domain_exception import DomainError

    usecase, persistence, _, _ = service()
    item = report()
    item.tests.append(item.tests[0])
    persistence.get_report_by_id.return_value = report()
    with pytest.raises(DomainError, match="unique"):
        if operation == "create":
            await usecase.create_report(item)
        else:
            await usecase.update_report(str(item.id), item)
    persistence.save_report.assert_not_awaited()
    persistence.update_report.assert_not_awaited()


async def test_report_status_update_preserves_fields_and_relations():
    usecase, persistence, samples, tests = service()
    item = report()
    persistence.get_report_by_id.return_value = item
    updated = await usecase.set_report_status(str(item.id), "Approved")
    assert updated.status == "Approved"
    assert updated.id == item.id
    assert updated.report_number == "FE 3157 - 361"
    assert updated.sample == domain_sample()
    assert updated.tests == [domain_test()]
    persistence.update_report.assert_awaited_once_with(item)
    samples.get_sample_by_id.assert_not_awaited()
    tests.get_test_by_id.assert_not_awaited()


async def test_missing_report_status_update_does_not_write():
    usecase, persistence, _, _ = service()
    persistence.get_report_by_id.return_value = None
    with pytest.raises(ReportNotFoundError):
        await usecase.set_report_status(str(uuid4()), "Approved")
    persistence.update_report.assert_not_awaited()
