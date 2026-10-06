"""Add the client relationship to users."""

import sqlalchemy as sa
from alembic import op

revision = "d7b8e9f0a1c2"
down_revision = "6a4d8c2e1f90"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("client_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        "fk_users_client_id_clients",
        "users",
        "clients",
        ["client_id"],
        ["id"],
    )
    op.create_index("ix_users_client_id", "users", ["client_id"])


def downgrade() -> None:
    op.drop_index("ix_users_client_id", table_name="users")
    op.drop_constraint(
        "fk_users_client_id_clients",
        "users",
        type_="foreignkey",
    )
    op.drop_column("users", "client_id")
