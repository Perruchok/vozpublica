import asyncpg
from typing import Optional
from backend.settings import (
    postgres_host,
    postgres_user,
    postgres_password,
    postgres_db,
    postgres_port
)
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}?sslmode=require"

# Database connection pool 
pool: Optional[asyncpg.Pool] = None


async def init_pool():
    """
    Initialize PostgreSQL connection pool.
    
    Optimized configuration for production with:
    - Minimum and maximum connections
    - Timeouts for complex queries
    - Connection rotation
    """
    global pool
    if pool is None:
        logger.info("Initializing database connection pool")
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=2,              # Minimum active connections
            max_size=10,             # Maximum connections
            max_inactive_connection_lifetime=300,  # 5 min - close inactive connections
            command_timeout=180,     # 3 min for complex queries (vectors)
            timeout=30,              # Timeout to get connection from pool
            max_queries=50000,       # Rotate connections every 50k queries
        )
        logger.info("Database connection pool initialized successfully", extra={
            "min_size": 2,
            "max_size": 10,
            "command_timeout": 180
        })
    return pool


async def get_pool() -> asyncpg.Pool:
    """
    Get connection pool (thread-safe).
    
    Returns:
        asyncpg.Pool: PostgreSQL connection pool
        
    Raises:
        Exception: If pool initialization fails
    """
    if pool is None:
        await init_pool()
    return pool


async def close_pool():
    """
    Close connection pool.
    
    Must be called on application shutdown to clean up resources.
    """
    global pool
    if pool:
        await pool.close()
        pool = None
        logger.info("Database connection pool closed")
