import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.output.postgresql.database.base import Base

if TYPE_CHECKING:
    from infrastructure.output.postgresql.entity.role_entity import RoleEntity
    from infrastructure.output.postgresql.entity.user_entity import UserEntity


class UserRoleEntity(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped["UserEntity"] = relationship(
        back_populates="user_roles",
    )

    role: Mapped["RoleEntity"] = relationship(
        back_populates="user_roles",
    )
