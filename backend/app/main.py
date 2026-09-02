from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from app.core.DB import ensure_indexes

from app.api.tailor import router as tailor_router
from app.api.parse_jd import router as jd_router
from app.api.v1.resume_workflow import (
    router as workflow_router
)
from app.api.v1.review import router as review_router
from app.api.v1.approval import router as approval_router
from app.api.v1.export import router as export_router
from app.api.v1.auth import router as auth_router

from app.core.config import settings
import os

from app.services.user_service import ensure_user_indexes
from app.services.database.usage_service import ensure_usage_indexes


os.environ["LANGSMITH_TRACING"] = str(
    settings.LANGSMITH_TRACING
).lower()

os.environ["LANGSMITH_ENDPOINT"] = (
    settings.LANGSMITH_ENDPOINT
)

os.environ["LANGSMITH_API_KEY"] = (
    settings.LANGSMITH_API_KEY
)

os.environ["LANGSMITH_PROJECT"] = (
    settings.LANGSMITH_PROJECT
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=settings.COOKIE_SECURE,
)

# update CORS: allow_credentials must be True, and origin can't be "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    ensure_indexes()
    ensure_user_indexes()
    ensure_usage_indexes()
    
#Routes 
app.include_router(auth_router)
app.include_router(review_router)
app.include_router(export_router)
app.include_router(approval_router)
app.include_router(workflow_router)
app.include_router(tailor_router,prefix="/api")
app.include_router(jd_router,prefix="/jd")


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
