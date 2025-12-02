"""Feature readiness gate.

FR-ENV-003: Feature MUST be marked as incomplete/non-operational until:
(a) .env file exists with real credential values (not placeholders), and
(b) the connectivity sanity-check passes for all external services.
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from core.connectivity import (
    ConnectivityChecker,
    ConnectivityReport,
    validate_env_config,
    EnvValidationResult,
)

logger = logging.getLogger(__name__)


@dataclass
class ReadinessResult:
    """Result of readiness check."""

    ready: bool
    env_valid: bool
    services_healthy: bool
    env_result: EnvValidationResult | None = None
    connectivity_report: ConnectivityReport | None = None
    message: str = ""


async def check_readiness() -> ReadinessResult:
    """Check if the application is ready to serve requests.

    Validates:
    1. Environment configuration has real values (not placeholders)
    2. All external services are reachable

    Returns:
        ReadinessResult with detailed status information.
    """
    # Check environment configuration
    env_vars = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "QDRANT_URL": os.environ.get("QDRANT_URL", ""),
        "QDRANT_API_KEY": os.environ.get("QDRANT_API_KEY", ""),
        "DATABASE_URL": os.environ.get("DATABASE_URL", ""),
    }
    env_result = validate_env_config(env_vars)

    if not env_result.is_valid:
        issues = []
        if env_result.missing:
            issues.append(f"Missing: {', '.join(env_result.missing)}")
        if env_result.placeholders:
            issues.append(f"Placeholders: {', '.join(env_result.placeholders)}")

        return ReadinessResult(
            ready=False,
            env_valid=False,
            services_healthy=False,
            env_result=env_result,
            message=f"Environment configuration invalid. {'; '.join(issues)}",
        )

    # Check service connectivity
    try:
        checker = ConnectivityChecker()
        report = await checker.check_all()
    except Exception as e:
        logger.exception("Error during connectivity check")
        return ReadinessResult(
            ready=False,
            env_valid=True,
            services_healthy=False,
            env_result=env_result,
            message=f"Connectivity check failed: {str(e)}",
        )

    if not report.all_healthy:
        unhealthy = []
        if not report.openai.healthy:
            unhealthy.append(f"OpenAI: {report.openai.message}")
        if not report.qdrant.healthy:
            unhealthy.append(f"Qdrant: {report.qdrant.message}")
        if not report.database.healthy:
            unhealthy.append(f"Database: {report.database.message}")

        return ReadinessResult(
            ready=False,
            env_valid=True,
            services_healthy=False,
            env_result=env_result,
            connectivity_report=report,
            message=f"Services unhealthy: {'; '.join(unhealthy)}",
        )

    return ReadinessResult(
        ready=True,
        env_valid=True,
        services_healthy=True,
        env_result=env_result,
        connectivity_report=report,
        message="All services healthy and ready",
    )


async def log_startup_status() -> ReadinessResult:
    """Log startup status and return readiness result.

    Called during application startup to log connectivity status.
    """
    logger.info("Checking application readiness...")

    result = await check_readiness()

    if result.ready:
        logger.info("✅ Application ready - all services healthy")
        if result.connectivity_report:
            if result.connectivity_report.openai.latency_ms:
                logger.info(
                    f"   OpenAI: {result.connectivity_report.openai.latency_ms:.0f}ms"
                )
            if result.connectivity_report.qdrant.latency_ms:
                logger.info(
                    f"   Qdrant: {result.connectivity_report.qdrant.latency_ms:.0f}ms"
                )
            if result.connectivity_report.database.latency_ms:
                logger.info(
                    f"   Database: {result.connectivity_report.database.latency_ms:.0f}ms"
                )
    else:
        logger.warning(f"⚠️  Application not ready: {result.message}")
        if not result.env_valid:
            logger.warning("   Please configure .env with valid credentials")

    return result
