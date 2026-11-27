"""Prevent more than one report from using the same sample."""

from alembic import op

revision = "a0eb1c2d3f45"
down_revision = "f9da0b2c3e4f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_reports_sample_id", table_name="reports")
    op.create_index("ix_reports_sample_id", "reports", ["sample_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_reports_sample_id", table_name="reports")
    op.create_index("ix_reports_sample_id", "reports", ["sample_id"])
