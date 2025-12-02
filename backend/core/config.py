"""Pydantic settings configuration.

Loads configuration from environment variables with validation.
"""

from functools import lru_cache
from typing import Any

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All required fields must be set via environment variables.
    Optional fields have sensible defaults for development.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="smart-humanoid-chatbot")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    log_level: str = Field(default="DEBUG")

    # API Server
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"]
    )

    # OpenAI Configuration (required)
    openai_api_key: SecretStr = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o")
    openai_embedding_model: str = Field(default="text-embedding-3-small")

    # Qdrant Vector Database (required)
    qdrant_url: str = Field(..., description="Qdrant cluster URL")
    qdrant_api_key: SecretStr = Field(..., description="Qdrant API key")
    qdrant_collection_name: str = Field(default="textbook_chunks")

    # Neon PostgreSQL Database (required)
    database_url: SecretStr = Field(..., description="PostgreSQL connection string")

    # RAG Pipeline Configuration
    rag_top_k: int = Field(default=10, ge=1, le=50)
    rag_similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    rag_max_citations: int = Field(default=5, ge=1, le=10)
    rag_max_context_tokens: int = Field(default=4000, ge=500, le=16000)

    # Session & Retention
    session_ttl_hours: int = Field(default=24, ge=1)
    message_retention_hours: int = Field(default=24, ge=1)

    # Safety Guardrails
    safety_keywords_enabled: bool = Field(default=True)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from JSON string or list."""
        if isinstance(v, str):
            import json

            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Treat as comma-separated if not valid JSON
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached Settings instance.

    Uses lru_cache to ensure singleton behavior - settings are loaded once
    and reused throughout the application lifecycle.
    """
    return Settings()
