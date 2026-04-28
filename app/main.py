from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware.error_handler import catch_exceptions_middleware
from app.routes.complaint_routes import router as complaint_router
from app.utils.logger import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="A production‑ready Complaint Management System API with JSON file storage.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "complaints",
            "description": "CRUD operations for complaints. Authentication optional.",
        },
    ],
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware (allow all origins by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
app.middleware("http")(catch_exceptions_middleware)

# Include routers
app.include_router(complaint_router, prefix="/api/v1", tags=["complaints"])

@app.get("/health", tags=["health"], summary="Health check")
async def health():
    return {"status": "ok"}