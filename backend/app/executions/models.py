from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Execution(Base):
    """
    One bounded execution run.

    This model records lifecycle only.
    It does NOT encode meaning, intelligence, or behavior.
    """

    __tablename__ = "executions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
        doc="started | completed | failed",
    )

    environment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Free-form environment description (OS, display, constraints)",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
  )
