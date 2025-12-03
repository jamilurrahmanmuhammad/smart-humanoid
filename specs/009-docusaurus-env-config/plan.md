# Implementation Plan: Docusaurus Environment Configuration

**Branch**: `009-docusaurus-env-config` | **Date**: 2025-12-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-docusaurus-env-config/spec.md`

## Summary

Externalize Docusaurus `url` and `baseUrl` configuration from hardcoded values to environment variables (`SITE_URL` and `BASE_URL`), enabling platform-agnostic deployment. Implementation uses Node.js `process.env` with fallback defaults and optional validation.

## Technical Context

**Language/Version**: TypeScript 5.x (Node.js 18+)
**Primary Dependencies**: Docusaurus 3.9.2, dotenv (optional devDependency)
**Storage**: N/A (configuration only)
**Testing**: Jest (config validation tests)
**Target Platform**: Node.js build environment, any hosting platform
**Project Type**: Single project (frontend documentation)
**Performance Goals**: N/A (build-time configuration)
**Constraints**: Must maintain backward compatibility with existing GitHub Pages deployment
**Scale/Scope**: Single config file modification, minimal scope

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| XIV. Infrastructure: Environment variables for secrets/config | **PASS** | Aligns - externalizing config to env vars |
| X. Technology Platform: No unnecessary dependencies | **PASS** | dotenv is optional; core uses native process.env |
| II. Code Quality: Tests required | **PASS** | TDD approach with Jest tests for config |
| VIII. Documentation: Deployment docs required | **PASS** | quickstart.md + .env.example included |

**All gates pass.** No constitution violations.

## Project Structure

### Documentation (this feature)

```text
specs/009-docusaurus-env-config/
├── plan.md              # This file
├── research.md          # Context7 Docusaurus research
├── data-model.md        # Configuration entities
├── quickstart.md        # Deployment engineer guide
├── contracts/           # N/A (no APIs)
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
# Config file modifications
docusaurus.config.ts     # Modify: Add env var support with defaults

# New files
.env.example             # Template for environment variables

# Test files (TDD approach)
tests/
└── config/
    └── env-config.test.ts  # Config validation tests
```

**Structure Decision**: Single project - minimal changes to existing Docusaurus config file. No new packages/modules needed. Test files added to verify configuration behavior.

## Implementation Approach (TDD)

### Phase 1: Red (Write Failing Tests)

1. Create test file `tests/config/env-config.test.ts`
2. Write tests for:
   - Default values used when env vars not set
   - `SITE_URL` environment variable overrides default
   - `BASE_URL` environment variable overrides default
   - Invalid URL format validation (missing protocol)
   - Invalid base URL validation (missing leading slash)

### Phase 2: Green (Make Tests Pass)

1. Modify `docusaurus.config.ts`:
   - Add optional dotenv import
   - Replace hardcoded `url` with `process.env.SITE_URL || 'http://localhost:3000'`
   - Replace hardcoded `baseUrl` with `process.env.BASE_URL || '/'`
   - Add validation helper functions

### Phase 3: Refactor

1. Extract validation logic to helper functions if needed
2. Create `.env.example` with documented variables
3. Update any existing documentation references

## Validation Logic

```typescript
// Validation helpers (to be implemented)
function validateUrl(url: string): string {
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    throw new Error(`Invalid SITE_URL: must start with http:// or https://`);
  }
  return url;
}

function validateBaseUrl(baseUrl: string): string {
  if (!baseUrl.startsWith('/')) {
    throw new Error(`Invalid BASE_URL: must start with /`);
  }
  return baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
}
```

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking existing GitHub Pages deployment | Keep GitHub Pages config (`organizationName`, `projectName`) as fallback |
| Build failures in CI/CD | Clear error messages with validation; documented .env.example |
| Developer confusion on local setup | Sensible defaults allow immediate local development |

## Complexity Tracking

> No constitution violations to justify.

N/A - Implementation is minimal and straightforward.

## Next Steps

1. Run `/sp.tasks` to generate task breakdown with TDD structure
2. Implement RED phase (failing tests)
3. Implement GREEN phase (make tests pass)
4. Create documentation and .env.example
