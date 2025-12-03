# Research: Docusaurus Environment Configuration

**Feature Branch**: `009-docusaurus-env-config`
**Date**: 2025-12-03
**Sources**: Context7 MCP (Docusaurus official documentation), docusaurus.io

## Summary

Docusaurus 3.x natively supports environment variables in configuration files through Node.js `process.env`. This is the official approach documented by Docusaurus.

## Key Findings

### 1. Environment Variable Support in docusaurus.config.js

From Docusaurus official documentation (Context7):

```javascript
// docusaurus.config.js
import 'dotenv/config';

export default {
  title: 'My Site',
  url: process.env.URL,
  baseUrl: process.env.BASE_URL,
  // ...
};
```

**Key points:**
- Config file runs in Node.js environment
- `process.env` access works directly
- Optional `dotenv` package enables `.env` file support for local development
- TypeScript configs (`.ts`) work the same way

### 2. Current State Analysis

Current `docusaurus.config.ts` (lines 18-21):
```typescript
url: 'https://jamilurrahmanmuhammad.github.io',
baseUrl: '/smart-humanoid/',
```

These are hardcoded values that need to be externalized.

### 3. Implementation Pattern

**Recommended pattern with defaults:**
```typescript
url: process.env.SITE_URL || 'http://localhost:3000',
baseUrl: process.env.BASE_URL || '/',
```

This pattern:
- Uses environment variable when set
- Falls back to sensible defaults for local development
- No code changes needed for different environments

### 4. dotenv Package (Optional)

For local development with `.env` files:

```bash
npm install dotenv
```

```typescript
// docusaurus.config.ts
import 'dotenv/config';
```

**Note**: This is optional. CI/CD systems typically inject environment variables directly.

### 5. Validation Considerations

Docusaurus validates `url` and `baseUrl` at build time:
- `url` must be a valid URL with protocol (http/https)
- `baseUrl` must start and end with `/`

Custom validation can be added in config file before Docusaurus receives values.

## Recommendations

1. **Pattern**: Use `process.env.VAR || 'default'` pattern
2. **dotenv**: Add as optional devDependency for local `.env` file support
3. **Validation**: Add helper function to validate URL format before use
4. **Documentation**: Create `.env.example` file showing required variables
5. **Testing**: Use Jest to test config file behavior with different env values

## References

- Docusaurus Configuration: https://docusaurus.io/docs/configuration
- Environment Variables in Node.js: https://nodejs.org/docs/latest/api/process.html#processenv
- dotenv package: https://www.npmjs.com/package/dotenv
