from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Database - usando alias para mapear variables PG* estándar
    postgres_host: str = Field(alias='PGHOST')
    postgres_port: int = Field(default=5432, alias='PGPORT')
    postgres_user: str = Field(alias='PGUSER')
    postgres_password: str = Field(alias='PGPASSWORD')
    postgres_db: str = Field(alias='PGDATABASE')

    # Azure OpenAI
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str
    azure_openai_embedding_deployment: str = "text-embedding-3-small"
    azure_openai_chat_deployment: str = "gpt-4.1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True  # permite usar tanto el nombre como el alias

settings = Settings()

# Exportar variables individuales para compatibilidad con código existente
postgres_host = settings.postgres_host
postgres_port = settings.postgres_port
postgres_user = settings.postgres_user
postgres_password = settings.postgres_password
postgres_db = settings.postgres_db

azure_openai_endpoint = settings.azure_openai_endpoint
azure_openai_api_key = settings.azure_openai_api_key
azure_openai_api_version = settings.azure_openai_api_version
azure_openai_embedding_deployment = settings.azure_openai_embedding_deployment
azure_openai_chat_deployment = settings.azure_openai_chat_deployment
