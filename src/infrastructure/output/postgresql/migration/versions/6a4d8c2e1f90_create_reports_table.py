"""Create reports and ordered test associations."""

import sqlalchemy as sa
from alembic import op

revision = "6a4d8c2e1f90"
down_revision = "c53e1f0a9b64"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("report_number", sa.String(100), nullable=False),
        sa.Column("report_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("sample_id", sa.UUID(), sa.ForeignKey("samples.id"), nullable=False),
    )
    op.create_index("ix_reports_sample_id", "reports", ["sample_id"])
    op.create_table(
        "report_tests",
        sa.Column(
            "report_id",
            sa.UUID(),
            sa.ForeignKey("reports.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("test_id", sa.UUID(), sa.ForeignKey("tests.id"), primary_key=True),
        sa.Column("position", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("report_tests")
    op.drop_index("ix_reports_sample_id", table_name="reports")
    op.drop_table("reports")
