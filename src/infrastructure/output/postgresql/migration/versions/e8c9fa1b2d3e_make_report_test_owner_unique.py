"""Ensure a test belongs to at most one report."""

from alembic import op

revision = "e8c9fa1b2d3e"
down_revision = "d7b8e9f0a1c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_report_tests_test_id", "report_tests", ["test_id"])


def downgrade() -> None:
    op.drop_constraint("uq_report_tests_test_id", "report_tests", type_="unique")
