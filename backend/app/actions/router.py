from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.actions.models import Action
from app.executions.models import Execution

router = APIRouter()


# ---------
# Schemas
# ---------

class ActionCreate(BaseModel):
    execution_id: str
    action_type: str
    parameters: str
    occurred_at: datetime | None = None


class ActionResponse(BaseModel):
    id: str
    execution_id: str
    action_type: str
    parameters: str
    occurred_at: datetime


# ---------
# Endpoints
# ---------

@router.post(
    "",
    response_model=ActionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_action(
    payload: ActionCreate,
    db: Session = Depends(get_db),
):
    # Ensure execution exists
    execution = db.get(Execution, payload.execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    action = Action(
        execution_id=payload.execution_id,
        action_type=payload.action_type,
        parameters=payload.parameters,
        occurred_at=payload.occurred_at or datetime.utcnow(),
    )

    db.add(action)
    db.commit()
    db.refresh(action)
    return action


@router.get(
    "/{execution_id}",
    response_model=list[ActionResponse],
)
def list_actions_for_execution(
    execution_id: str,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Action)
        .filter(Action.execution_id == execution_id)
        .order_by(Action.occurred_at.asc())
        .all()
    )
    return rows
