from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.users import Users

from core.dbconnect import Base

class Project(Base):
    __tablename__ = 'project'

    id : Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id : Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
        index=True
    )

    user : Mapped['Users'] = relationship(
        back_populates='projects'
    )

    name : Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    repository_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )