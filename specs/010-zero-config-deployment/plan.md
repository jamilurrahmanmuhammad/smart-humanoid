# Implementation Plan: Zero-Config Platform Deployment

**Branch**: `010-zero-config-deployment` | **Date**: 2025-12-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-zero-config-deployment/spec.md`
**Approach**: TDD (Test-Driven Development)

## Summary

Enable zero-configuration deployment of the Smart Humanoid documentation site by relying solely on industry-standard Node.js conventions. The project will use package.json scripts, engines field, and CI environment variable detection (CI=true) to automatically configure for any standards-compliant hosting platform without platform-specific configuration files.

## Technical Context

**Language/Version**: TypeScript 5.6+ / Node.js 20+
**Primary Dependencies**: Docusaurus 3.9.2, React 19, existing config-helpers.ts from feature 009
**Storage**: N/A (static site generation)
**Testing**: Jest 30+ with ts-jest (existing from feature 009)
**Target Platform**: Any static site hosting platform that follows Node.js conventions
**Project Type**: Single (Docusaurus static site)
**Performance Goals**: Build < 5 minutes, dev server start < 30 seconds
**Constraints**: No platform-specific config files (vercel.json, netlify.toml, etc.)
**Scale/Scope**: Single documentation site, multiple potential deployment platforms

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| X. Content Delivery | PASS | Docusaurus 3.x + GitHub Pages/Vercel deployment aligned |
| XIV. Infrastructure Principles | PASS | No hardcoded secrets; env vars for configuration |
| VIII. Technical Accuracy | PASS | Code must work; using TDD approach |
| XXXVIII. Content Review Gates | N/A | Infrastructure feature, not content |

**Gate Status**: PASS - No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/010-zero-config-deployment/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (minimal - config entities)
├── quickstart.md        # Phase 1 output (deployment guide)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Existing structure - minimal changes required
config-helpers.ts        # MODIFY: Add CI detection logic
docusaurus.config.ts     # VERIFY: Already uses config-helpers
package.json             # VERIFY/MODIFY: Ensure engines field, standard scripts

# Test structure (existing from feature 009)
tests/
└── config/
    └── env-config.test.ts  # EXTEND: Add CI detection tests
```

**Structure Decision**: Minimal changes to existing structure. Primary work is enhancing `config-helpers.ts` with CI environment detection and ensuring `package.json` follows industry standards.

## Architecture Overview

### Environment Detection Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Build Environment                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Check CI=true env var (industry standard)                   │
│     ├── If true → CI/Production build mode                      │
│     └── If false/missing → Local development mode               │
│                                                                  │
│  2. Check SITE_URL env var (from feature 009)                   │
│     ├── If set → Use provided URL                               │
│     └── If missing + CI=true → Use sensible default             │
│     └── If missing + local → Use http://localhost:3000          │
│                                                                  │
│  3. Check BASE_URL env var (from feature 009)                   │
│     ├── If set → Use provided base path                         │
│     └── If missing → Default to /                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Industry-Standard Configuration

**package.json requirements** (platforms auto-detect these):
- `engines.node`: ">=20.0" - specifies minimum Node.js version
- `scripts.build`: "docusaurus build" - standard build command
- `scripts.start`: "docusaurus start" - standard dev command
- Output directory: `build/` - Docusaurus default, widely recognized

**No platform-specific files needed**:
- vercel.json
- netlify.toml
- render.yaml
- etc.

### CI Environment Variable Detection

The `CI` environment variable is set to `true` by virtually all CI/CD systems:
- GitHub Actions: `CI=true`
- GitLab CI: `CI=true`
- CircleCI: `CI=true`
- Travis CI: `CI=true`
- Jenkins: `CI=true`
- Vercel: `CI=true`
- Netlify: `CI=true`
- Cloudflare Pages: `CI=true`

This provides technology-agnostic detection without platform-specific code.

## TDD Implementation Strategy

### Phase: RED (Write Failing Tests First)

1. Test: `isCI()` returns true when CI=true
2. Test: `isCI()` returns false when CI not set
3. Test: `getConfig()` in CI mode with no SITE_URL uses sensible behavior
4. Test: `getConfig()` in local mode uses localhost defaults
5. Test: package.json has required engines field
6. Test: package.json has required scripts

### Phase: GREEN (Make Tests Pass)

1. Add `isCI()` function to config-helpers.ts
2. Update `getConfig()` to use CI detection
3. Verify/update package.json with engines field

### Phase: REFACTOR

1. Ensure documentation is clear
2. Update .env.example with CI detection notes
3. Create deployment quickstart guide

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CI detection | CI=true env var | Industry standard across all platforms |
| URL detection | SITE_URL + BASE_URL | Already implemented in feature 009 |
| Config files | None platform-specific | User requirement for industry-standard only |
| Build output | build/ directory | Docusaurus default, widely recognized |
| Node version | >=20.0 in engines | Modern LTS, specified in package.json |

## Complexity Tracking

> No constitution violations requiring justification.

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| Changes | Minimal | Extends existing config-helpers.ts |
| Testing | TDD | All changes test-driven |
| Dependencies | None new | Uses existing dependencies |

## Dependencies on Previous Features

- **Feature 009 (docusaurus-env-config)**: Provides `config-helpers.ts` with `validateUrl()`, `validateBaseUrl()`, and `getConfig()` functions
- This feature extends that foundation with CI environment detection

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Platform doesn't set CI=true | Low | Fallback to URL-based detection from feature 009 |
| Platform uses non-standard build command | Low | Document in quickstart.md |
| Build output directory mismatch | Low | Docusaurus default `build/` is widely recognized |

## Success Validation

1. **Local**: `npm run build` works without env vars
2. **CI simulation**: `CI=true npm run build` works
3. **Platform test**: Import repo to a hosting platform, verify zero-config deployment
