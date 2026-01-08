import asyncpg

from backend.settings import (
    postgres_host,
    postgres_user,
    postgres_password,
    postgres_db,
    postgres_port
)

DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}?sslmode=require"

# Database connection pool 
pool = None
async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=180  # Increased timeout for complex vector queries
        )
    return pool