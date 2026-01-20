from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import qa, search, semantic_evolution, explain_drift, health
from backend.__version__ import __version__, API_VERSION, API_TITLE, API_DESCRIPTION, REPOSITORY
from backend.utils.logger import setup_logger
from backend.utils.dbpool import get_pool, close_pool
from dotenv import load_dotenv
from typing import List
import os

# Load environment variables from .env file
load_dotenv()

# Setup logger
logger = setup_logger(__name__)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=__version__,
    contact={
        "name": "VozPublica Team",
        "url": REPOSITORY,
    },
    license_info={
        "name": "MIT",
    },
)


def get_allowed_origins() -> List[str]:
    """
    Gets allowed origins based on the environment.
    In production: only specific domains from environment variable.
    In development: localhost and any GitHub Codespaces domain.
    """
    environment = os.getenv("ENVIRONMENT", "production")
    
    if environment == "development":
        return [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "https://*.app.github.dev",  # GitHub Codespaces
        ]
    
    # Production: use ALLOWED_ORIGINS environment variable
    allowed = os.getenv("ALLOWED_ORIGINS", "")
    if not allowed:
        logger.warning("ALLOWED_ORIGINS not set in production environment")
        return []
    
    origins = [origin.strip() for origin in allowed.split(",") if origin.strip()]
    return origins


# CORS configuration
allowed_origins = get_allowed_origins()

# In development, use permissive CORS; in production, require explicit configuration
if os.getenv("ENVIRONMENT") == "development":
    if not allowed_origins:
        allowed_origins = ["*"]
        logger.warning("Development mode: Using wildcard CORS for all origins")
    else:
        # In dev, append wildcard to support dynamic environments like Codespaces
        if "*" not in allowed_origins:
            allowed_origins.append("*")
else:
    if not allowed_origins:
        logger.error("No CORS origins configured. Set ALLOWED_ORIGINS environment variable.")

logger.info(f"CORS Configuration: {len(allowed_origins)} allowed origins", 
           extra={"origins": allowed_origins, "environment": os.getenv("ENVIRONMENT", "production")})

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["Content-Type"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include routers
app.include_router(health.router)  # Health checks without prefix
app.include_router(qa.router, prefix=f"/api/{API_VERSION}")
app.include_router(search.router, prefix=f"/api/{API_VERSION}")
app.include_router(semantic_evolution.router, prefix=f"/api/{API_VERSION}")
app.include_router(explain_drift.router, prefix=f"/api/{API_VERSION}")


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    logger.info("Starting VozPública API", extra={
        "version": __version__,
        "api_version": API_VERSION,
        "environment": os.getenv("ENVIRONMENT", "production")
    })
    
    # Warm up database pool
    try:
        pool = await get_pool()
        logger.info("Database connection pool initialized", extra={
            "min_size": pool._minsize,
            "max_size": pool._maxsize
        })
    except Exception as e:
        logger.error("Failed to initialize database pool", extra={"error": str(e)})
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down VozPública API")
    
    # Close connection pool
    try:
        await close_pool()
        logger.info("Database connection pool closed")
    except Exception as e:
        logger.error("Error closing database pool", extra={"error": str(e)})


@app.get("/")
async def root():
    return {
        "message": API_TITLE,
        "version": __version__,
        "api_version": API_VERSION,
        "environment": os.getenv("ENVIRONMENT", "production"),
        "docs": "/docs",
        "repository": REPOSITORY,
        "endpoints": {
            "health": "/health",
            "health_detailed": "/health/detailed",
            "api": f"/api/{API_VERSION}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
