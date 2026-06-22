"""create sample types table

Revision ID: d14f6e9b3c72
Revises: 0442a7645526
Create Date: 2026-06-22

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d14f6e9b3c72"
down_revision: str | Sequence[str] | None = "0442a7645526"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sample_types",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sample_types_name"), "sample_types", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sample_types_name"), table_name="sample_types")
    op.drop_table("sample_types")
