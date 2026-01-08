from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import qa, search, semantic_evolution, explain_drift
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Voz Pública API")

# CORS configuration for frontend
# Get Codespace frontend URL from environment
import os

codespace_name = os.getenv("CODESPACE_NAME")

# En desarrollo, permitir todos los orígenes para debug
# TODO: Restringir en producción
allowed_origins = ["*"]

# Configuración alternativa más restrictiva (comentada por ahora):
# allowed_origins = [
#     "http://localhost:3000",
#     "http://localhost:3001",
# ]
# if codespace_name:
#     github_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")
#     allowed_origins.extend([
#         f"https://{codespace_name}-3000.{github_domain}",
#         f"https://{codespace_name}-3001.{github_domain}",
#     ])

print(f"🔧 CORS Configuration:")
print(f"   Codespace Name: {codespace_name}")
print(f"   Allowed Origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
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
