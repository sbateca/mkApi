from dataclasses import replace
from uuid import UUID, uuid4

import pytest

from application.dto.request import ReportRequestDto
from application.mapper.report_mapper import ReportMapper
from domain.exception.analysis_method_exception import AnalysisMethodNotFoundError
from domain.exception.analyte_exception import AnalyteNotFoundError
from domain.exception.criteria_exception import CriteriaNotFoundError
from domain.exception.report_exception import (
    ReportActionDeniedError,
    ReportNotFoundError,
)
from domain.exception.sample_exception import SampleNotFoundError
from domain.exception.test_type_exception import (
    TestTypeNotFoundError as MissingTestTypeError,
)
from domain.model.authenticated_user import AuthenticatedUser
from domain.model.authorization_action import AuthorizationAction
from domain.model.authorization_resource import AuthorizationResource
from domain.model.authorization_scope import AuthorizationScope
from domain.policy.action_policy import ActionPolicy
from domain.util.constants import ResourceType, UserRole
from tests.builders.report_builder import admin, body, report, service
from tests.builders.report_sample_builder import (
    domain_sample,
)
from tests.builders.report_test_builder import domain_test


async def test_report_crud_resolves_relations_and_preserves_identity():
    usecase, persistence, _, tests = service()
    item = ReportMapper().to_report(ReportRequestDto(**body()))
    created = await usecase.create_report(item, admin())
    assert created.id is not None
    assert created.sample == domain_sample()
    assert created.tests == [domain_test()]
    persistence.save_report.assert_awaited_once_with(
        created, report_tests_port=usecase.report_test_persistence_port
    )
    persistence.get_report_by_id.return_value = created
    persistence.get_reports.return_value = [created]
    actor = AuthenticatedUser(uuid4(), frozenset({UserRole.ADMIN}))
    listed = await usecase.get_reports(actor)
    assert [item.id for item in listed] == [created.id]
    assert listed[0].actions["read"].allowed
    changed = report()
    changed.report_number = "Updated"
    changed.tests = []
    updated = await usecase.update_report(str(created.id), changed, actor)
    assert updated.id == created.id
    assert updated.tests == []
    await usecase.delete_report(str(created.id), actor)
    persistence.delete_report.assert_awaited_once_with(str(created.id))


@pytest.mark.parametrize(
    ("port_name", "method", "error"),
    [
        ("sample_persistence_port", "get_sample_by_id", SampleNotFoundError),
        (
            "analysis_method_persistence_port",
            "get_analysis_method_by_id",
            AnalysisMethodNotFoundError,
        ),
        ("analyte_persistence_port", "get_analyte_by_id", AnalyteNotFoundError),
        ("criteria_persistence_port", "get_criteria_by_id", CriteriaNotFoundError),
        ("test_type_persistence_port", "get_test_type_by_id", MissingTestTypeError),
    ],
)
async def test_report_invalid_relations_do_not_write(port_name, method, error):
    usecase, persistence, _, tests = service()
    getattr(getattr(usecase, port_name), method).return_value = None
    with pytest.raises(error):
        await usecase.create_report(report(), admin())
    persistence.save_report.assert_not_awaited()


async def test_report_missing_blocks_read_update_delete():
    usecase, persistence, _, _ = service()
    persistence.get_report_by_id.return_value = None
    for operation in [
        usecase.get_report_by_id("missing", admin()),
        usecase.update_report("missing", report(), admin()),
        usecase.delete_report("missing", admin()),
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
            await usecase.create_report(item, admin())
        else:
            await usecase.update_report(str(item.id), item, admin())
    persistence.save_report.assert_not_awaited()
    persistence.update_report.assert_not_awaited()


async def test_report_status_update_preserves_fields_and_relations():
    usecase, persistence, samples, tests = service()
    item = report()
    persistence.get_report_by_id.return_value = item
    updated = await usecase.set_report_status(str(item.id), "Approved", admin())
    assert updated.status == "Approved"
    assert updated.id == item.id
    assert updated.report_number == "FE 3157 - 361"
    assert updated.sample == domain_sample()
    assert updated.tests == [domain_test()]
    persistence.update_report_status.assert_awaited_once_with(str(item.id), "Approved")
    samples.get_sample_by_id.assert_not_awaited()


async def test_missing_report_status_update_does_not_write():
    usecase, persistence, _, _ = service()
    persistence.get_report_by_id.return_value = None
    with pytest.raises(ReportNotFoundError):
        await usecase.set_report_status(str(uuid4()), "Approved", admin())
    persistence.update_report_status.assert_not_awaited()


async def test_client_report_listing_is_filtered_in_persistence():
    usecase, persistence, _, _ = service()
    client_id = UUID("63cc2808-29d7-4c84-aa9f-feca7792a893")
    actor = AuthenticatedUser(uuid4(), frozenset({UserRole.CLIENT}), client_id)
    usecase.authorization_port.get_scope.return_value = AuthorizationScope.OWN
    persistence.get_reports_by_client_id.return_value = [report()]

    result = await usecase.get_reports(actor)

    assert [item.id for item in result] == [
        item.id for item in persistence.get_reports_by_client_id.return_value
    ]
    persistence.get_reports_by_client_id.assert_awaited_once_with(client_id)
    persistence.get_reports.assert_not_awaited()


async def test_report_update_denied_before_persistence():
    usecase, persistence, _, _ = service()
    usecase.authorization_port.is_allowed.return_value = False
    item = report()
    persistence.get_report_by_id.return_value = item
    with pytest.raises(ReportActionDeniedError):
        await usecase.update_report(str(item.id), item, admin())
    persistence.update_report.assert_not_awaited()


async def test_create_and_update_cannot_approve_report():
    usecase, persistence, _, _ = service()
    actor = admin()
    item = report()
    item.status = "Approved"

    created = await usecase.create_report(item, actor)
    assert created.status == "Draft"

    persistence.get_report_by_id.return_value = created
    edited = report()
    edited.status = "Approved"
    assert (
        await usecase.update_report(str(created.id), edited, actor)
    ).status == "Draft"
    persistence.update_report_status.assert_not_awaited()


@pytest.mark.parametrize(
    ("owns_report", "status", "denied_code"),
    [
        (True, "Draft", "report_not_approved"),
        (True, "Approved", None),
        (True, "Issued", "report_not_approved"),
        (False, "Approved", "forbidden"),
    ],
)
async def test_report_download_requires_perm_and_approval(
    owns_report, status, denied_code
):
    from infrastructure.configuration.dependencies import get_authorization_port

    usecase, persistence, _, _ = service()
    usecase.action_policy = ActionPolicy(get_authorization_port())
    item = report()
    item.status = status
    persistence.get_report_by_id.return_value = item
    client_id = item.sample.client.id if owns_report else uuid4()
    actor = AuthenticatedUser(uuid4(), frozenset({UserRole.CLIENT}), client_id)

    if owns_report:
        detail = await usecase.get_report_by_id(str(item.id), actor)
        assert detail.actions["download"].allowed is (denied_code is None)
        assert detail.actions["download"].code == denied_code
    else:
        with pytest.raises(ReportActionDeniedError, match="forbidden"):
            await usecase.get_report_by_id(str(item.id), actor)

    if denied_code:
        with pytest.raises(ReportActionDeniedError, match=denied_code):
            await usecase.get_report_for_download(str(item.id), actor)
    else:
        assert await usecase.get_report_for_download(str(item.id), actor) is item


@pytest.mark.parametrize(
    "role", [role for role in UserRole if role is not UserRole.CLIENT]
)
async def test_internal_roles_can_download_any_approved_report(role):
    from infrastructure.configuration.dependencies import get_authorization_port

    usecase, persistence, _, _ = service()
    usecase.action_policy = ActionPolicy(get_authorization_port())
    item = report()
    persistence.get_report_by_id.return_value = item
    actor = AuthenticatedUser(uuid4(), frozenset({role}))

    item.status = "Draft"
    with pytest.raises(ReportActionDeniedError, match="report_not_approved"):
        await usecase.get_report_for_download(str(item.id), actor)

    item.status = "Approved"
    assert await usecase.get_report_for_download(str(item.id), actor) is item


@pytest.mark.parametrize("status", ["Approved", "Issued"])
async def test_non_draft_report_mutations_are_disabled(status):
    usecase, persistence, _, _ = service()
    item = report()
    item.status = status
    persistence.get_report_by_id.return_value = item
    actor = admin()
    report_id = str(item.id)
    detail = await usecase.get_report_by_id(report_id, actor)

    for action, operation in (
        ("update", usecase.update_report(report_id, report(), actor)),
        ("delete", usecase.delete_report(report_id, actor)),
        ("approve", usecase.set_report_status(report_id, "Approved", actor)),
    ):
        assert not detail.actions[action].allowed
        assert detail.actions[action].code == "report_not_draft"
        with pytest.raises(ReportActionDeniedError, match="report_not_draft"):
            await operation

    persistence.update_report.assert_not_awaited()
    persistence.delete_report.assert_not_awaited()
    persistence.update_report_status.assert_not_awaited()


@pytest.mark.parametrize(
    "roles",
    [frozenset({UserRole.CLIENT}), frozenset({UserRole.CLIENT, UserRole.ADMIN})],
)
async def test_client_cannot_edit_or_delete_own_draft_report(roles):
    from infrastructure.configuration.dependencies import get_authorization_port

    usecase, persistence, _, _ = service()
    usecase.action_policy = ActionPolicy(get_authorization_port())
    item = report()
    persistence.get_report_by_id.return_value = item
    actor = AuthenticatedUser(uuid4(), roles, item.sample.client.id)
    report_id = str(item.id)
    detail = await usecase.get_report_by_id(report_id, actor)

    for action, operation in (
        ("update", usecase.update_report(report_id, report(), actor)),
        ("delete", usecase.delete_report(report_id, actor)),
    ):
        assert not detail.actions[action].allowed
        assert detail.actions[action].code == "forbidden"
        with pytest.raises(ReportActionDeniedError, match="forbidden"):
            await operation

    persistence.update_report.assert_not_awaited()
    persistence.delete_report.assert_not_awaited()


@pytest.mark.parametrize("can_edit_destination", [True, False])
async def test_report_update_uses_saved_status_when_moving_to_another_client(
    can_edit_destination,
):
    usecase, persistence, samples, _ = service()
    current = report()
    current.status = "Draft"
    persistence.get_report_by_id.return_value = current
    destination_client = replace(current.sample.client, id=uuid4())
    destination = replace(current.sample, id=uuid4(), client=destination_client)
    samples.get_sample_by_id.return_value = destination
    usecase.authorization_port.is_allowed.side_effect = [True, can_edit_destination]

    edited = replace(current, status="Approved", sample=destination, tests=[])
    actor = admin()
    if can_edit_destination:
        updated = await usecase.update_report(str(current.id), edited, actor)
        assert updated.status == current.status
        assert updated.sample.id == destination.id
        persistence.update_report.assert_awaited_once_with(updated)
    else:
        with pytest.raises(ReportActionDeniedError, match="forbidden"):
            await usecase.update_report(str(current.id), edited, actor)
        persistence.update_report.assert_not_awaited()

    assert [
        call.args for call in usecase.authorization_port.is_allowed.call_args_list
    ] == [
        (
            actor,
            AuthorizationAction.UPDATE,
            AuthorizationResource(ResourceType.REPORT, client_id),
        )
        for client_id in (current.sample.client.id, destination_client.id)
    ]
