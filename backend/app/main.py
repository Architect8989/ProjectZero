from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers (will be implemented incrementally)
from app.executions.router import router as executions_router
from app.observations.router import router as observations_router
from app.actions.router import router as actions_router
from app.artifacts.router import router as artifacts_router
from app.audit.router import router as audit_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="UI Execution Backend",
        description="Control plane for UI-level execution, observations, and proof artifacts.",
        version="0.1.0",
    )

    # CORS (open for now, restrict later)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check — FIRST reality endpoint
    @app.get("/health", tags=["system"])
    def health_check():
        return {"status": "ok"}

    # Register routers (even if empty for now)
    app.include_router(executions_router, prefix="/executions", tags=["executions"])
    app.include_router(observations_router, prefix="/observations", tags=["observations"])
    app.include_router(actions_router, prefix="/actions", tags=["actions"])
    app.include_router(artifacts_router, prefix="/artifacts", tags=["artifacts"])
    app.include_router(audit_router, prefix="/audit", tags=["audit"])

    return app


app = create_app()
