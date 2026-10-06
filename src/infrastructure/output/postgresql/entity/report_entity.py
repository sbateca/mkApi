from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.output.postgresql.database.base import Base
from infrastructure.output.postgresql.entity.sample_entity import SampleEntity
from infrastructure.output.postgresql.entity.test_entity import TestEntity

report_tests = Table(
    "report_tests",
    Base.metadata,
    Column("report_id", ForeignKey("reports.id", ondelete="CASCADE"), primary_key=True),
    Column("test_id", ForeignKey("tests.id"), primary_key=True),
    Column("position", Integer, nullable=False),
)


class ReportEntity(Base):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    report_number: Mapped[str] = mapped_column(String(100), nullable=False)
    report_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    sample_id: Mapped[UUID] = mapped_column(
        ForeignKey("samples.id"), index=True, nullable=False
    )
    sample: Mapped[SampleEntity] = relationship()
    tests: Mapped[list[TestEntity]] = relationship(
        secondary=report_tests, order_by=report_tests.c.position, viewonly=True
    )
