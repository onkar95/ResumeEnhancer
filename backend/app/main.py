from fastapi import FastAPI

from app.api.tailor import router as tailor_router
from app.api.parse_jd import router as jd_router
from app.core.config import settings
from app.api.v1.resume_workflow import (
    router as workflow_router
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(
    workflow_router
)

app.include_router(
    tailor_router,
    prefix="/api"
)
app.include_router(
    jd_router,
    prefix="/jd"
    )

@app.get("/")
def root():
    return {
        "message": settings.APP_NAME
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
    

