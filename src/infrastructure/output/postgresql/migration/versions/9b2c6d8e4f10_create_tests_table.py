"""create tests table

Revision ID: 9b2c6d8e4f10
Revises: f1a2b3c4d5e6
Create Date: 2026-07-09

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9b2c6d8e4f10"
down_revision: str | Sequence[str] | None = "f1a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tests",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("test_type_id", sa.UUID(), nullable=False),
        sa.Column("sample_id", sa.UUID(), nullable=False),
        sa.Column("analyte_id", sa.UUID(), nullable=False),
        sa.Column("analysis_method_id", sa.UUID(), nullable=False),
        sa.Column("criteria_id", sa.UUID(), nullable=False),
        sa.Column("result", sa.String(length=150), nullable=False),
        sa.ForeignKeyConstraint(["analysis_method_id"], ["analysis_methods.id"]),
        sa.ForeignKeyConstraint(["analyte_id"], ["analytes.id"]),
        sa.ForeignKeyConstraint(["criteria_id"], ["criteria.id"]),
        sa.ForeignKeyConstraint(["sample_id"], ["samples.id"]),
        sa.ForeignKeyConstraint(["test_type_id"], ["test_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tests_sample_id"), "tests", ["sample_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tests_sample_id"), table_name="tests")
    op.drop_table("tests")
