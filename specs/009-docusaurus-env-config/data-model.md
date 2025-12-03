# Data Model: Docusaurus Environment Configuration

**Feature Branch**: `009-docusaurus-env-config`
**Date**: 2025-12-03

## Overview

This feature involves configuration values only - no persistent data storage. The "data model" describes the configuration entities and their constraints.

## Configuration Entities

### 1. Site URL (`SITE_URL`)

| Property | Value |
|----------|-------|
| **Type** | String (URL) |
| **Environment Variable** | `SITE_URL` |
| **Default** | `http://localhost:3000` |
| **Required** | No (has default) |
| **Format** | Full URL with protocol |

**Constraints:**
- Must start with `http://` or `https://`
- Must be a valid URL format
- No trailing slash required

**Examples:**
```
https://docs.example.com
https://company.github.io
http://localhost:3000
```

### 2. Base URL (`BASE_URL`)

| Property | Value |
|----------|-------|
| **Type** | String (Path) |
| **Environment Variable** | `BASE_URL` |
| **Default** | `/` |
| **Required** | No (has default) |
| **Format** | Path starting with `/` |

**Constraints:**
- Must start with `/`
- Trailing slash optional (normalized internally)
- Cannot contain query strings or fragments

**Examples:**
```
/
/docs/
/smart-humanoid/
/v2/documentation/
```

## Validation Rules

| Rule ID | Field | Validation | Error Message |
|---------|-------|------------|---------------|
| V-001 | SITE_URL | Starts with http:// or https:// | "Invalid SITE_URL: must start with http:// or https://" |
| V-002 | BASE_URL | Starts with / | "Invalid BASE_URL: must start with /" |
| V-003 | BASE_URL | Normalized to end with / | (automatic, no error) |

## Configuration Resolution Order

```
1. Environment variable (SITE_URL, BASE_URL)
   ↓ if not set
2. Default value (localhost:3000, /)
```

## Relationship to Docusaurus Config

```typescript
// docusaurus.config.ts mapping
{
  url: SITE_URL,      // Full canonical URL
  baseUrl: BASE_URL,  // Path prefix

  // These remain for backward compatibility
  organizationName: 'jamilurrahmanmuhammad',
  projectName: 'smart-humanoid',
}
```

## No Database Entities

This feature does not create, modify, or interact with any database. All configuration is resolved at build time from environment variables.
