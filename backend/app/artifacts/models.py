from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Artifact(Base):
    """
    Immutable proof artifact produced by an execution.

    Examples:
    - screenshot_before
    - screenshot_after
    - delta
    - video_recording

    Artifacts are evidence. They are never modified or deleted.
    """

    __tablename__ = "artifacts"

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

    artifact_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        doc="before | after | delta | video | log",
    )

    storage_uri: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Object storage URI (S3/GCS/MinIO/etc)",
    )

    checksum: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        doc="Hash for integrity verification",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


Index("ix_artifacts_execution_type", Artifact.execution_id, Artifact.artifact_type)
