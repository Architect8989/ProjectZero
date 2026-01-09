"""
Database initialization script.

Creates all tables defined in SQLAlchemy models.
Run this ONCE before starting the backend.
"""

from app.db.session import engine
from app.db.base import Base

# Import all models so they are registered with SQLAlchemy metadata
from app.executions.models import Execution
from app.observations.models import Observation
from app.actions.models import Action
from app.artifacts.models import Artifact
from app.audit.models import AuditEvent


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
