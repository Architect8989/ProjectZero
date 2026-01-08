from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Observation(Base):
    """
    Raw perception record.
    No interpretation. No intelligence.
    This is ground truth: what the screen looked like at a moment in time.
    """

    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    execution_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
        doc="FK to executions.id",
    )

    storage_uri: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Object storage URI for the screenshot/frame",
    )

    checksum: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        doc="Hash of the frame for immutability verification",
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


Index("ix_observations_execution_time", Observation.execution_id, Observation.captured_at)
