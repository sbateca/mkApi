"""create criteria table

Revision ID: e4f7b2d91480
Revises: d14f6e9b3c72
Create Date: 2026-06-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e4f7b2d91480"
down_revision: str | Sequence[str] | None = "d14f6e9b3c72"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "criteria",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_criteria_name"), "criteria", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_criteria_name"), table_name="criteria")
    op.drop_table("criteria")
