from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.dbconnect import Base

class Project(Base):
    __tablename__ = 'project'

    id : Mapped[int] = mapped_column(
        primary_key=True,
        index=True
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