from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.output.postgresql.database.base import Base

if TYPE_CHECKING:
    from infrastructure.output.postgresql.entity.client_entity import ClientEntity
    from infrastructure.output.postgresql.entity.sample_type_entity import (
        SampleTypeEntity,
    )


class SampleEntity(Base):
    __tablename__ = "samples"

    id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    sample_code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    sample_type_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("sample_types.id"),
        nullable=False,
    )
    client_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("clients.id"),
        nullable=False,
    )
    get_sample_date: Mapped[date] = mapped_column(Date, nullable=False)
    reception_date: Mapped[date] = mapped_column(Date, nullable=False)
    analysis_date: Mapped[date] = mapped_column(Date, nullable=False)
    sample_location: Mapped[str] = mapped_column(String(250), nullable=False)
    responsable: Mapped[str] = mapped_column(String(150), nullable=False)

    sample_type: Mapped["SampleTypeEntity"] = relationship()
    client: Mapped["ClientEntity"] = relationship()
