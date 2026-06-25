"""create samples table

Revision ID: f1a2b3c4d5e6
Revises: e4f7b2d91480
Create Date: 2026-06-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f1a2b3c4d5e6"
down_revision: str | Sequence[str] | None = "e4f7b2d91480"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "samples",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("sample_code", sa.String(length=50), nullable=False),
        sa.Column("sample_type_id", sa.UUID(), nullable=False),
        sa.Column("client_id", sa.UUID(), nullable=False),
        sa.Column("get_sample_date", sa.Date(), nullable=False),
        sa.Column("reception_date", sa.Date(), nullable=False),
        sa.Column("analysis_date", sa.Date(), nullable=False),
        sa.Column("sample_location", sa.String(length=250), nullable=False),
        sa.Column("responsable", sa.String(length=150), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["sample_type_id"], ["sample_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_samples_sample_code"), "samples", ["sample_code"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_samples_sample_code"), table_name="samples")
    op.drop_table("samples")
