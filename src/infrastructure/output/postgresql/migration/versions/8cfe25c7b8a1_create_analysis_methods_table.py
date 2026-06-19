"""create analysis methods table

Revision ID: 8cfe25c7b8a1
Revises: 58c0aee544e6
Create Date: 2026-06-18

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8cfe25c7b8a1"
down_revision: str | Sequence[str] | None = "58c0aee544e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "analysis_methods",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_analysis_methods_name"),
        "analysis_methods",
        ["name"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_analysis_methods_name"), table_name="analysis_methods")
    op.drop_table("analysis_methods")
