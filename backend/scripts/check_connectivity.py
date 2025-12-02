#!/usr/bin/env python
"""Connectivity sanity-check script.

FR-ENV-002: Verifies successful connection to all external services
(OpenAI, Qdrant, Neon PostgreSQL) before the application is considered operational.

Usage:
    python scripts/check_connectivity.py

Returns exit code 0 if all services healthy, 1 otherwise.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env file
from dotenv import load_dotenv
load_dotenv()


async def main() -> int:
    """Run connectivity checks and print report.

    Returns:
        0 if all services healthy, 1 otherwise.
    """
    from core.connectivity import (
        ConnectivityChecker,
        validate_env_config,
    )
    import os

    print("=" * 60)
    print("RAG Chatbot Connectivity Check")
    print("=" * 60)
    print()

    # First validate .env configuration
    print("1. Validating environment configuration...")
    env_vars = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "QDRANT_URL": os.environ.get("QDRANT_URL", ""),
        "QDRANT_API_KEY": os.environ.get("QDRANT_API_KEY", ""),
        "DATABASE_URL": os.environ.get("DATABASE_URL", ""),
    }
    env_result = validate_env_config(env_vars)

    if not env_result.is_valid:
        print("   ❌ Environment configuration invalid!")
        if env_result.missing:
            print(f"   Missing variables: {', '.join(env_result.missing)}")
        if env_result.placeholders:
            print(f"   Placeholder values detected: {', '.join(env_result.placeholders)}")
        print()
        print("   Please configure .env file with real credentials.")
        print("   See .env.example for required variables.")
        return 1

    print("   ✅ Environment configuration valid")
    print()

    # Run connectivity checks
    print("2. Checking service connectivity...")
    print()

    checker = ConnectivityChecker()
    report = await checker.check_all()

    # Print individual service status
    services = [
        ("OpenAI API", report.openai),
        ("Qdrant Vector DB", report.qdrant),
        ("PostgreSQL Database", report.database),
    ]

    for name, status in services:
        icon = "✅" if status.healthy else "❌"
        latency = f" ({status.latency_ms:.0f}ms)" if status.latency_ms else ""
        print(f"   {icon} {name}: {status.message}{latency}")

    print()
    print("=" * 60)

    if report.all_healthy:
        print("✅ All services healthy - Application ready!")
        return 0
    else:
        print("❌ Some services unavailable - Check configuration")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
