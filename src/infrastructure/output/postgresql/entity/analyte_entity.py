from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.output.postgresql.database.base import Base

if TYPE_CHECKING:
    from infrastructure.output.postgresql.entity.test_type_entity import TestTypeEntity


ANALYTE_NAME_TEST_TYPE_INDEX = "ix_analytes_name_test_type_id"


class AnalyteEntity(Base):
    __tablename__ = "analytes"
    __table_args__ = (
        Index(ANALYTE_NAME_TEST_TYPE_INDEX, "name", "test_type_id", unique=True),
    )

    id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    test_type_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("test_types.id"),
        nullable=False,
    )

    test_type: Mapped["TestTypeEntity"] = relationship(
        back_populates="analytes",
    )
