from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Action(Base):
    """
    Concrete action that occurred on the OS.

    This records WHAT happened, not WHY.
    No intent. No prediction. No intelligence.
    """

    __tablename__ = "actions"

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

    action_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        doc="mouse_move | mouse_click | key_press | key_release",
    )

    parameters: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Serialized parameters (e.g. x,y,button,key)",
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


Index("ix_actions_execution_time", Action.execution_id, Action.occurred_at)
