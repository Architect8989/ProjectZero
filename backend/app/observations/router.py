from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.observations.models import Observation
from app.executions.models import Execution

router = APIRouter()


# ---------
# Schemas
# ---------

class ObservationCreate(BaseModel):
    execution_id: str
    storage_uri: HttpUrl | str
    checksum: str
    captured_at: datetime | None = None


class ObservationResponse(BaseModel):
    id: str
    execution_id: str
    storage_uri: str
    checksum: str
    captured_at: datetime


# ---------
# Endpoints
# ---------

@router.post(
    "",
    response_model=ObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_observation(
    payload: ObservationCreate,
    db: Session = Depends(get_db),
):
    # Ensure execution exists
    execution = db.get(Execution, payload.execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    obs = Observation(
        execution_id=payload.execution_id,
        storage_uri=str(payload.storage_uri),
        checksum=payload.checksum,
        captured_at=payload.captured_at or datetime.utcnow(),
    )

    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs


@router.get(
    "/{execution_id}",
    response_model=list[ObservationResponse],
)
def list_observations_for_execution(
    execution_id: str,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Observation)
        .filter(Observation.execution_id == execution_id)
        .order_by(Observation.captured_at.asc())
        .all()
    )
    return rows
