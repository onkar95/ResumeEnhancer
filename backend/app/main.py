from fastapi import FastAPI, HTTPException, logger
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from app.services.pdf_export_service import get_browser
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

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

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

# main.py


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


# @app.on_event("startup")
# async def on_startup():
#     try:
#         ensure_indexes()
#         ensure_user_indexes()
#         ensure_usage_indexes()
#         await get_browser()
#     except Exception as e:
#         logger.exception("Failed to initialize Playwright: %s", e)


@app.on_event("shutdown")
async def on_shutdown():
    global _browser, _playwright
    if _browser:
        await _browser.close()
    if _playwright:
        await _playwright.stop()

# Routes
app.include_router(auth_router)
app.include_router(review_router)
app.include_router(export_router)
app.include_router(approval_router)
app.include_router(workflow_router)
app.include_router(tailor_router, prefix="/api")
app.include_router(jd_router, prefix="/jd")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Invalid request",
                 "error": exc.errors()},
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
