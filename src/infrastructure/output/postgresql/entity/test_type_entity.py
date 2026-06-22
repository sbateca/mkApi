from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.output.postgresql.database.base import Base

if TYPE_CHECKING:
    from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity


class TestTypeEntity(Base):
    __tablename__ = "test_types"

    id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True
    )

    analytes: Mapped[list["AnalyteEntity"]] = relationship(
        back_populates="test_type",
        cascade="all, delete-orphan",
    )
