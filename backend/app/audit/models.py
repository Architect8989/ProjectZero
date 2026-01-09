from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditEvent(Base):
    """
    Immutable audit log entry.

    Append-only.
    No updates.
    No deletes.

    This is the system of record for:
    - who did what
    - when
    - against which object
    """

    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    actor_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        doc="user | executor | system",
    )

    actor_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        doc="Identifier of the actor (if applicable)",
    )

    action: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        doc="Action performed (e.g. execution_started, artifact_uploaded)",
    )

    target_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        doc="execution | observation | action | artifact",
    )

    target_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        doc="ID of the target object",
    )

    metadata: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional JSON-serialized metadata",
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


Index("ix_audit_time", AuditEvent.occurred_at)
Index("ix_audit_target", AuditEvent.target_type, AuditEvent.target_id)
