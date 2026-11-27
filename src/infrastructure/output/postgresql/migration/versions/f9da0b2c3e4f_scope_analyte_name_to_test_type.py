"""Make analyte names unique within each test type."""

from alembic import op

revision = "f9da0b2c3e4f"
down_revision = "e8c9fa1b2d3e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_analytes_name_test_type_id",
        "analytes",
        ["name", "test_type_id"],
        unique=True,
    )
    op.drop_index("ix_analytes_name", table_name="analytes")


def downgrade() -> None:
    op.create_index("ix_analytes_name", "analytes", ["name"], unique=True)
    op.drop_index("ix_analytes_name_test_type_id", table_name="analytes")
