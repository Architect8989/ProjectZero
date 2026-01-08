from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.executions.models import Execution

router = APIRouter()


# ---------
# Schemas
# ---------

class ExecutionStartRequest(BaseModel):
    environment: str | None = None


class ExecutionResponse(BaseModel):
    id: str
    status: str
    environment: str | None
    started_at: datetime
    finished_at: datetime | None


# ---------
# Endpoints
# ---------

@router.post(
    "/start",
    response_model=ExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_execution(
    payload: ExecutionStartRequest,
    db: Session = Depends(get_db),
):
    execution = Execution(
        id=str(uuid4()),
        status="started",
        environment=payload.environment,
        started_at=datetime.utcnow(),
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution


@router.post(
    "/{execution_id}/complete",
    response_model=ExecutionResponse,
)
def complete_execution(
    execution_id: str,
    success: bool,
    db: Session = Depends(get_db),
):
    execution = db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    execution.status = "completed" if success else "failed"
    execution.finished_at = datetime.utcnow()

    db.commit()
    db.refresh(execution)

    return execution


@router.get(
    "/{execution_id}",
    response_model=ExecutionResponse,
)
def get_execution(
    execution_id: str,
    db: Session = Depends(get_db),
):
    execution = db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return execution
