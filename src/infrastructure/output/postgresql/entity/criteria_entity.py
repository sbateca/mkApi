from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.output.postgresql.database.base import Base


class CriteriaEntity(Base):
    __tablename__ = "criteria"

    id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True
    )
