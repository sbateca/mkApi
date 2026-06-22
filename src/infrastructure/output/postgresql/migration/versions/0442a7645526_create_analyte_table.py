"""Create Analyte table

Revision ID: 0442a7645526
Revises: b7a9d41e2f63
Create Date: 2026-06-19 13:23:00.941018

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0442a7645526"
down_revision: str | Sequence[str] | None = "b7a9d41e2f63"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "analytes",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column("test_type_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["test_type_id"], ["test_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_analytes_name"), "analytes", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_analytes_name"), table_name="analytes")
    op.drop_table("analytes")
