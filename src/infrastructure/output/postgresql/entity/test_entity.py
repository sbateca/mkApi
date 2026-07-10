from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.output.postgresql.database.base import Base

if TYPE_CHECKING:
    from infrastructure.output.postgresql.entity.analysis_method_entity import (
        AnalysisMethodEntity,
    )
    from infrastructure.output.postgresql.entity.analyte_entity import AnalyteEntity
    from infrastructure.output.postgresql.entity.criteria_entity import CriteriaEntity
    from infrastructure.output.postgresql.entity.test_type_entity import TestTypeEntity


class TestEntity(Base):
    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    test_type_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("test_types.id"),
        nullable=False,
    )
    sample_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("samples.id"),
        nullable=False,
        index=True,
    )
    analyte_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("analytes.id"),
        nullable=False,
    )
    analysis_method_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("analysis_methods.id"),
        nullable=False,
    )
    criteria_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("criteria.id"),
        nullable=False,
    )
    result: Mapped[str] = mapped_column(String(150), nullable=False)

    test_type: Mapped["TestTypeEntity"] = relationship()
    analyte: Mapped["AnalyteEntity"] = relationship()
    analysis_method: Mapped["AnalysisMethodEntity"] = relationship()
    criteria: Mapped["CriteriaEntity"] = relationship()
