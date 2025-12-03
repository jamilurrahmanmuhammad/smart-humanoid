# Data Model: Zero-Config Platform Deployment

**Feature**: 010-zero-config-deployment
**Date**: 2025-12-03

## Overview

This feature has a minimal data model focused on configuration entities. No database storage is involved - all configuration is read from environment variables at build time.

## Entities

### UrlConfig (existing from feature 009)

Configuration object for Docusaurus URL settings.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| url | string | Yes | Full site URL (e.g., `https://example.com`) |
| baseUrl | string | Yes | Base path (e.g., `/` or `/docs/`) |

**Validation Rules**:
- `url` must start with `http://` or `https://`
- `baseUrl` must start with `/`
- `baseUrl` normalized to have trailing slash (except for `/`)

### EnvironmentContext (new)

Represents the detected build environment.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| isCI | boolean | Yes | Whether running in CI/CD environment |
| isBuild | boolean | Yes | Whether running a build (vs dev server) |

**Detection Logic**:
- `isCI`: `process.env.CI === 'true'`
- `isBuild`: Determined by Docusaurus command context

## Environment Variables

### CI Detection (industry standard)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| CI | string | undefined | Set to `'true'` by CI/CD platforms |

### URL Configuration (from feature 009)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| SITE_URL | string | `http://localhost:3000` | Full site URL |
| BASE_URL | string | `/` | Base path for site |

## Configuration Priority

```
1. Explicit env vars (SITE_URL, BASE_URL) - highest priority
2. CI detection (CI=true) - informs logging/warnings
3. Built-in defaults - lowest priority (localhost)
```

## State Transitions

This feature has no runtime state - all configuration is resolved at build time.

```
┌──────────────────────────────────────────────────┐
│              Build Time Resolution               │
├──────────────────────────────────────────────────┤
│                                                  │
│  Start Build                                     │
│       │                                          │
│       ▼                                          │
│  Read Environment Variables                      │
│       │                                          │
│       ├── CI=true? ──► Log "CI mode detected"   │
│       │                                          │
│       ├── SITE_URL set? ──► Use provided URL    │
│       │      │                                   │
│       │      └── No ──► Use default localhost   │
│       │                                          │
│       ├── BASE_URL set? ──► Use provided path   │
│       │      │                                   │
│       │      └── No ──► Use default /           │
│       │                                          │
│       ▼                                          │
│  Validate URLs                                   │
│       │                                          │
│       ├── Valid ──► Continue build              │
│       │                                          │
│       └── Invalid ──► Throw error with message  │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Relationships

```
package.json
    │
    ├── engines.node ──► Specifies Node.js version for platforms
    │
    ├── scripts.build ──► Build command for platforms
    │
    └── scripts.start ──► Dev command for local development

config-helpers.ts
    │
    ├── isCI() ──► Detects CI environment
    │
    ├── getConfig() ──► Returns UrlConfig
    │
    └── validateUrl() / validateBaseUrl() ──► Validation helpers

docusaurus.config.ts
    │
    └── imports getConfig() ──► Uses url and baseUrl
```

## No Database Required

This feature operates entirely at build time with no persistent storage needs.
