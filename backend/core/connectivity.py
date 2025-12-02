"""Connectivity sanity-check utility for external services.

FR-ENV-002: System MUST provide connectivity sanity-check that verifies
successful connection to all three external services (OpenAI, Qdrant, Neon).
"""

import os
import re
import time
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI
from qdrant_client import QdrantClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from core.config import get_settings


@dataclass
class ServiceStatus:
    """Status of a single service connection."""

    healthy: bool
    message: str
    latency_ms: Optional[float] = None


@dataclass
class ConnectivityReport:
    """Report of all service connection statuses."""

    openai: ServiceStatus
    qdrant: ServiceStatus
    database: ServiceStatus

    @property
    def all_healthy(self) -> bool:
        """Return True if all services are healthy."""
        return self.openai.healthy and self.qdrant.healthy and self.database.healthy


@dataclass
class EnvValidationResult:
    """Result of environment configuration validation."""

    is_valid: bool
    missing: list[str] = field(default_factory=list)
    placeholders: list[str] = field(default_factory=list)


# Common placeholder patterns
PLACEHOLDER_PATTERNS = [
    r"^your[-_]",
    r"[-_]here$",
    r"^YOUR_",
    r"^xxx",
    r"placeholder",
    r"^$",  # empty string
]


def is_placeholder_value(value: str) -> bool:
    """Check if a value appears to be a placeholder rather than a real credential.

    Args:
        value: The environment variable value to check.

    Returns:
        True if the value looks like a placeholder.
    """
    if not value or not value.strip():
        return True

    value_lower = value.lower()
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, value_lower):
            return True

    return False


def validate_env_config(env_vars: dict[str, str]) -> EnvValidationResult:
    """Validate that all required environment variables have real values.

    Args:
        env_vars: Dictionary of environment variable names to values.

    Returns:
        EnvValidationResult with validation status and any issues found.
    """
    required_keys = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "DATABASE_URL"]

    missing = []
    placeholders = []

    for key in required_keys:
        if key not in env_vars:
            missing.append(key)
        elif is_placeholder_value(env_vars[key]):
            placeholders.append(key)

    return EnvValidationResult(
        is_valid=len(missing) == 0 and len(placeholders) == 0,
        missing=missing,
        placeholders=placeholders,
    )


class ConnectivityChecker:
    """Service for checking connectivity to external dependencies."""

    def __init__(self) -> None:
        """Initialize the connectivity checker with settings."""
        self.settings = get_settings()

    async def check_openai(self) -> ServiceStatus:
        """Check OpenAI API connectivity.

        Returns:
            ServiceStatus with connection result.
        """
        try:
            start_time = time.time()
            # Get the actual string value from SecretStr
            api_key = self.settings.openai_api_key.get_secret_value()
            client = OpenAI(api_key=api_key)
            # Simple API call to verify key is valid
            client.models.list()
            latency_ms = (time.time() - start_time) * 1000

            return ServiceStatus(
                healthy=True,
                message="OpenAI API connected successfully",
                latency_ms=latency_ms,
            )
        except Exception as e:
            return ServiceStatus(
                healthy=False,
                message=f"OpenAI API error: {str(e)}",
            )

    async def check_qdrant(self) -> ServiceStatus:
        """Check Qdrant vector database connectivity.

        Returns:
            ServiceStatus with connection result.
        """
        try:
            start_time = time.time()
            # Get the actual string value from SecretStr
            api_key = self.settings.qdrant_api_key.get_secret_value()
            client = QdrantClient(
                url=self.settings.qdrant_url,
                api_key=api_key,
            )
            # Simple call to verify connection
            client.get_collections()
            latency_ms = (time.time() - start_time) * 1000

            return ServiceStatus(
                healthy=True,
                message="Qdrant connected successfully",
                latency_ms=latency_ms,
            )
        except Exception as e:
            return ServiceStatus(
                healthy=False,
                message=f"Qdrant error: {str(e)}",
            )

    async def check_database(self) -> ServiceStatus:
        """Check PostgreSQL database connectivity.

        Returns:
            ServiceStatus with connection result.
        """
        try:
            import ssl
            start_time = time.time()
            # Get the actual string value from SecretStr
            db_url = self.settings.database_url.get_secret_value()

            # Strip any query parameters that asyncpg doesn't understand
            if "?" in db_url:
                db_url = db_url.split("?")[0]

            # Create SSL context for Neon (requires SSL)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            engine = create_async_engine(
                db_url,
                echo=False,
                connect_args={"ssl": ssl_context},
            )

            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            latency_ms = (time.time() - start_time) * 1000
            await engine.dispose()

            return ServiceStatus(
                healthy=True,
                message="Database connected successfully",
                latency_ms=latency_ms,
            )
        except Exception as e:
            return ServiceStatus(
                healthy=False,
                message=f"Database error: {str(e)}",
            )

    async def check_all(self) -> ConnectivityReport:
        """Check connectivity to all services.

        Returns:
            ConnectivityReport with status for all services.
        """
        openai_status = await self.check_openai()
        qdrant_status = await self.check_qdrant()
        database_status = await self.check_database()

        return ConnectivityReport(
            openai=openai_status,
            qdrant=qdrant_status,
            database=database_status,
        )


async def run_connectivity_check() -> ConnectivityReport:
    """Run connectivity check and return report.

    Convenience function for scripts.
    """
    checker = ConnectivityChecker()
    return await checker.check_all()
