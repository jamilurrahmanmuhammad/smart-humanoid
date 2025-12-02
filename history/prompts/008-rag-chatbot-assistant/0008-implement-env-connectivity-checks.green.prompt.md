---
id: 0008
title: Implement Environment Connectivity Checks
stage: green
date: 2025-12-02
surface: agent
model: claude-opus-4-5-20251101
feature: 008-rag-chatbot-assistant
branch: 008-rag-chatbot-assistant
user: jamil
command: continue
labels: [FR-ENV-001, FR-ENV-002, FR-ENV-003, connectivity, readiness, TDD]
links:
  spec: specs/008-rag-chatbot-assistant/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/008-rag-chatbot-assistant/tasks.md
  - specs/008-rag-chatbot-assistant/spec.md
  - backend/core/connectivity.py
  - backend/core/readiness.py
  - backend/scripts/check_connectivity.py
  - backend/api/routes/health.py
  - backend/main.py
  - backend/tests/unit/test_connectivity.py
tests:
  - tests/unit/test_connectivity.py (14 tests)
---

## Prompt

continue..

(Continuation of previous session which updated spec.md with FR-ENV requirements)

## Response snapshot

Implemented environment configuration validation and connectivity checks per new FR-ENV requirements:

1. **Updated tasks.md** - Added T003a, T003b, T003c for environment configuration:
   - T003a [RED]: Write test for connectivity sanity-check utility
   - T003b [GREEN]: Implement connectivity sanity-check script
   - T003c: Implement feature readiness gate

2. **Created core/connectivity.py** - Connectivity checker with:
   - `ServiceStatus` and `ConnectivityReport` dataclasses
   - `ConnectivityChecker` class with check_openai(), check_qdrant(), check_database()
   - `is_placeholder_value()` and `validate_env_config()` for .env validation
   - `run_connectivity_check()` convenience function

3. **Created core/readiness.py** - Feature readiness gate:
   - `ReadinessResult` dataclass with detailed status
   - `check_readiness()` async function checking env + services
   - `log_startup_status()` for startup logging

4. **Created scripts/check_connectivity.py** - CLI script for checking connectivity

5. **Updated api/routes/health.py** - Enhanced /ready endpoint:
   - Now checks env_config validity
   - Reports all service statuses (openai, qdrant, database)
   - Returns unhealthy/degraded/healthy based on comprehensive checks

6. **Updated main.py** - Added startup logging:
   - Calls `log_startup_status()` on startup
   - Logs warning if app starts in degraded mode

7. **Created tests/unit/test_connectivity.py** - 14 tests covering:
   - ServiceStatus and ConnectivityReport dataclasses
   - ConnectivityChecker for each service
   - Environment validation (placeholder detection, missing vars)

## Outcome

- ✅ Impact: FR-ENV-001, FR-ENV-002, FR-ENV-003 now implemented with TDD
- 🧪 Tests: 140 passing (14 new connectivity tests added)
- 📁 Files: 7 files created/modified
- 🔁 Next prompts: Create .env with real credentials, run connectivity check, populate Qdrant
- 🧠 Reflection: Gap analysis from previous session correctly identified missing environment validation - now addressed with comprehensive checks

## Evaluation notes (flywheel)

- Failure modes observed: Test fixture needed proper lru_cache clearing via get_settings.cache_clear()
- Graders run and results (PASS/FAIL): All 140 tests PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Configure real .env and run scripts/check_connectivity.py
