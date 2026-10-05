"""Add refresh token families and replacement lineage.

Revision ID: c53e1f0a9b64
Revises: b42d0e9f8a53
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c53e1f0a9b64"
down_revision: str | Sequence[str] | None = "b42d0e9f8a53"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("refresh_tokens", sa.Column("family_id", sa.UUID(), nullable=True))
    op.add_column(
        "refresh_tokens",
        sa.Column("replaced_by_token_id", sa.UUID(), nullable=True),
    )
    op.execute("UPDATE refresh_tokens SET family_id = id WHERE family_id IS NULL")
    op.alter_column("refresh_tokens", "family_id", nullable=False)
    op.create_foreign_key(
        "fk_refresh_tokens_replaced_by_token_id",
        "refresh_tokens",
        "refresh_tokens",
        ["replaced_by_token_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_refresh_tokens_family_id", "refresh_tokens", ["family_id"])


def downgrade() -> None:
    op.drop_index("ix_refresh_tokens_family_id", table_name="refresh_tokens")
    op.drop_constraint(
        "fk_refresh_tokens_replaced_by_token_id",
        "refresh_tokens",
        type_="foreignkey",
    )
    op.drop_column("refresh_tokens", "replaced_by_token_id")
    op.drop_column("refresh_tokens", "family_id")
