from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.audit.models import AuditEvent

router = APIRouter()


# ---------
# Schemas
# ---------

class AuditEventResponse(BaseModel):
    id: str
    actor_type: str
    actor_id: str | None
    action: str
    target_type: str
    target_id: str
    metadata: str | None
    occurred_at: str


# ---------
# Endpoints
# ---------

@router.get(
    "/events",
    response_model=list[AuditEventResponse],
)
def list_audit_events(
    db: Session = Depends(get_db),
):
    """
    Read-only access to audit events.
    No filters for now. No deletes. No writes.
    """
    rows = (
        db.query(AuditEvent)
        .order_by(AuditEvent.occurred_at.desc())
        .all()
    )
    return rows
