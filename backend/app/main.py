from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import qa, search, semantic_evolution, explain_drift
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Voz Pública API")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(semantic_evolution.router, prefix="/api")
app.include_router(explain_drift.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "message": "VozPublica API",
        "version": "1.0",
        "docs": "/docs"
    }
