"""
Health check endpoints for Azure Web Service.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from backend.utils.dbpool import get_pool
from backend.settings import settings
from backend.__version__ import __version__
from openai import AzureOpenAI
import asyncio
from typing import Dict, Any
import time

router = APIRouter(tags=["health"])


async def check_database() -> Dict[str, Any]:
    """
    Check PostgreSQL connectivity and performance.
    
    Returns:
        Dict with status, response_time_ms and optionally error
    """
    start_time = time.time()
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            # Simple query to verify connectivity
            result = await conn.fetchval("SELECT 1")
            response_time = (time.time() - start_time) * 1000  # ms
            
            if result == 1:
                return {
                    "status": "healthy",
                    "response_time_ms": round(response_time, 2),
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": "Unexpected query result"
                }
    except asyncio.TimeoutError:
        return {
            "status": "unhealthy",
            "error": "Database connection timeout"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


async def check_openai() -> Dict[str, Any]:
    """
    Check Azure OpenAI configuration.
    Does not make API calls to avoid consuming quota.
    
    Returns:
        Dict with status and optionally error
    """
    try:
        # Validate that environment variables are configured
        if not settings.azure_openai_endpoint:
            return {
                "status": "misconfigured",
                "error": "AZURE_OPENAI_ENDPOINT not set"
            }
        
        if not settings.azure_openai_api_key:
            return {
                "status": "misconfigured",
                "error": "AZURE_OPENAI_API_KEY not set"
            }
        
        # Instantiate client (does not make API calls)
        client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        
        return {
            "status": "configured",
            "endpoint": settings.azure_openai_endpoint,
            "api_version": settings.azure_openai_api_version,
            "embedding_deployment": settings.azure_openai_embedding_deployment,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@router.get("/health")
async def health_check():
    """
    Basic health check for Azure Web Service.
    
    This endpoint must respond quickly (< 1s) and return 200 if the service is up.
    Azure uses it to determine if the container is ready to receive traffic.
    
    Returns:
        200 OK with status: "ok"
    """
    return {"status": "ok", "version": __version__}


@router.get("/health/detailed")
async def health_check_detailed():
    """
    Detailed health check with dependency verification.
    
    Verifies:
    - PostgreSQL connectivity
    - Azure OpenAI configuration
    
    Returns:
        200 OK if all dependencies are healthy
        503 Service Unavailable if any dependency fails
    """
    # Execute checks in parallel
    results = await asyncio.gather(
        check_database(),
        check_openai(),
        return_exceptions=True
    )
    
    db_health, openai_health = results
    
    # Determine overall state
    overall_healthy = (
        isinstance(db_health, dict) and db_health.get("status") == "healthy" and
        isinstance(openai_health, dict) and openai_health.get("status") == "configured"
    )
    
    response = {
        "status": "healthy" if overall_healthy else "degraded",
        "version": __version__,
        "dependencies": {
            "database": db_health if isinstance(db_health, dict) else {"status": "error", "error": str(db_health)},
            "azure_openai": openai_health if isinstance(openai_health, dict) else {"status": "error", "error": str(openai_health)},
        }
    }
    
    status_code = status.HTTP_200_OK if overall_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(content=response, status_code=status_code)


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness probe for Kubernetes/Azure Container Apps.
    
    Verifies that the service is ready to accept traffic.
    Similar to /health/detailed but with shorter timeout.
    
    Returns:
        200 OK if the service is ready
        503 Service Unavailable if not ready
    """
    # Only verify database (critical for operation)
    try:
        db_health = await asyncio.wait_for(check_database(), timeout=5.0)
        
        if db_health.get("status") == "healthy":
            return {"status": "ready"}
        else:
            return JSONResponse(
                content={"status": "not_ready", "reason": db_health.get("error")},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    except asyncio.TimeoutError:
        return JSONResponse(
            content={"status": "not_ready", "reason": "Database check timeout"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@router.get("/health/live")
async def liveness_check():
    """
    Liveness probe for Kubernetes/Azure Container Apps.
    
    Verifies that the process is alive (not blocked).
    Only returns 200 if the process can respond.
    
    Returns:
        200 OK always (if it can respond)
    """
    return {"status": "alive"}
