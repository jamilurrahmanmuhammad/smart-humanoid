# Research: Zero-Config Platform Deployment

**Feature**: 010-zero-config-deployment
**Date**: 2025-12-03
**Sources**: Context7 Docusaurus documentation, industry standards

## Research Questions

### RQ1: How do hosting platforms detect Node.js projects?

**Decision**: Rely on `package.json` with standard scripts and `engines` field.

**Rationale**: All major hosting platforms scan for `package.json` to identify Node.js projects. They auto-detect:
- Build command from `scripts.build`
- Dev command from `scripts.start`
- Node version from `engines.node`
- Output directory from framework detection (Docusaurus → `build/`)

**Alternatives Considered**:
- Platform-specific config files (vercel.json, netlify.toml) - REJECTED per user requirement
- Custom build scripts - REJECTED, adds complexity without benefit

**Evidence** (from Context7):
```json
{
  "scripts": {
    "start": "docusaurus start",
    "build": "docusaurus build"
  }
}
```

### RQ2: How to detect CI/deployment environment universally?

**Decision**: Use `CI=true` environment variable.

**Rationale**: The `CI` environment variable is the de facto industry standard, set automatically by:
- GitHub Actions
- GitLab CI
- CircleCI
- Travis CI
- Jenkins
- Vercel
- Netlify
- Cloudflare Pages
- Azure DevOps
- AWS CodeBuild

This is technology-agnostic and works for any language/framework.

**Alternatives Considered**:
- Check for platform-specific env vars (VERCEL, NETLIFY) - REJECTED per user requirement
- Check NODE_ENV=production - REJECTED, not as universally set
- No detection, always same defaults - REJECTED, doesn't enable auto-configuration

**Evidence**: Industry documentation confirms CI=true is standard across platforms.

### RQ3: What Docusaurus config values need environment-based configuration?

**Decision**: `url` and `baseUrl` only (already implemented in feature 009).

**Rationale**: From Context7 Docusaurus documentation:
```javascript
export default {
  url: 'https://docusaurus-2.netlify.app',
  baseUrl: '/',
};
```

These are the only values that vary between local development and production deployment.

**Alternatives Considered**:
- Configure more settings via env vars - REJECTED, unnecessary complexity
- Hardcode production values - REJECTED, breaks local development

**Evidence** (from existing config-helpers.ts):
```typescript
export function getConfig(): UrlConfig {
  const rawUrl = process.env.SITE_URL || 'http://localhost:3000';
  const rawBaseUrl = process.env.BASE_URL || '/';
  return {
    url: validateUrl(rawUrl),
    baseUrl: validateBaseUrl(rawBaseUrl),
  };
}
```

### RQ4: What is the standard build output directory?

**Decision**: Use Docusaurus default `build/` directory.

**Rationale**: Docusaurus outputs to `build/` by default, which is:
- Recognized by all major hosting platforms
- Standard for static site generators
- No configuration needed

**Alternatives Considered**:
- Custom output directory - REJECTED, adds unnecessary configuration
- `dist/` directory - REJECTED, not Docusaurus default

### RQ5: How should the project handle missing SITE_URL in CI?

**Decision**: In CI mode without SITE_URL, continue to use localhost default but log a warning.

**Rationale**:
- Platforms that provide deployment URLs will set SITE_URL
- Platforms that don't will still build successfully
- The warning helps users understand they may need to set SITE_URL manually

**Alternatives Considered**:
- Fail build if CI=true but no SITE_URL - REJECTED, too strict for testing
- Guess URL from platform env vars - REJECTED per user requirement (no platform-specific code)

## Summary of Decisions

| Topic | Decision | Key Rationale |
|-------|----------|---------------|
| Project detection | package.json + engines | Industry standard |
| CI detection | CI=true env var | Universal across platforms |
| Config values | url + baseUrl via SITE_URL/BASE_URL | Already implemented in feature 009 |
| Build output | build/ (Docusaurus default) | Recognized by all platforms |
| Missing SITE_URL in CI | Log warning, use default | Graceful degradation |

## Implementation Implications

1. **Minimal code changes**: Extend existing `config-helpers.ts` with `isCI()` function
2. **No new dependencies**: All functionality uses built-in Node.js APIs
3. **TDD approach**: Write tests for CI detection before implementation
4. **Documentation**: Create quickstart.md for deployment guidance

## References

1. Docusaurus Deployment Documentation (via Context7)
2. Docusaurus Configuration API (via Context7)
3. CI Environment Variable Standard (industry practice)
