"""create test types table

Revision ID: b7a9d41e2f63
Revises: 8cfe25c7b8a1
Create Date: 2026-06-19

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b7a9d41e2f63"
down_revision: str | Sequence[str] | None = "8cfe25c7b8a1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "test_types",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_types_name"), "test_types", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_test_types_name"), table_name="test_types")
    op.drop_table("test_types")
