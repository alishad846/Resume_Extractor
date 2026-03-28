"""FastAPI main application entry point for Resume AI Platform."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.api import auth, resumes, extraction, scoring, search, feedback, jd_mgmt, analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events."""
    # Startup
    logger.info("🚀 Resume AI Platform starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Resume AI Platform shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Resume AI Platform",
    description="Advanced resume processing and ATS system with AI-powered insights",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }


# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resume Management"])
app.include_router(extraction.router, prefix="/api/extraction", tags=["NLP Extraction"])
app.include_router(scoring.router, prefix="/api/scoring", tags=["Resume Scoring"])
app.include_router(search.router, prefix="/api/search", tags=["Semantic Search"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["AI Feedback"])
app.include_router(jd_mgmt.router, prefix="/api/jd", tags=["Job Descriptions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with platform info."""
    return {
        "name": "Resume AI Platform",
        "version": "1.0.0",
        "description": "Advanced resume processing and ATS system",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "api": "/api"
        }
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "error": "Internal server error",
        "detail": str(exc) if settings.ENVIRONMENT == "development" else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
