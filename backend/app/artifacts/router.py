from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.artifacts.models import Artifact
from app.executions.models import Execution

router = APIRouter()


# ---------
# Schemas
# ---------

class ArtifactCreate(BaseModel):
    execution_id: str
    artifact_type: str
    storage_uri: HttpUrl | str
    checksum: str


class ArtifactResponse(BaseModel):
    id: str
    execution_id: str
    artifact_type: str
    storage_uri: str
    checksum: str
    created_at: str


# ---------
# Endpoints
# ---------

@router.post(
    "",
    response_model=ArtifactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_artifact(
    payload: ArtifactCreate,
    db: Session = Depends(get_db),
):
    # Ensure execution exists
    execution = db.get(Execution, payload.execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    artifact = Artifact(
        execution_id=payload.execution_id,
        artifact_type=payload.artifact_type,
        storage_uri=str(payload.storage_uri),
        checksum=payload.checksum,
    )

    db.add(artifact)
    db.commit()
    db.refresh(artifact)
    return artifact


@router.get(
    "/{execution_id}",
    response_model=list[ArtifactResponse],
)
def list_artifacts_for_execution(
    execution_id: str,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Artifact)
        .filter(Artifact.execution_id == execution_id)
        .order_by(Artifact.created_at.asc())
        .all()
    )
    return rows
