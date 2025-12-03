# Quickstart: Docusaurus Environment Configuration

**Audience**: DevOps / Deployment Engineers

---

## TL;DR - Deploy in 3 Steps

```bash
# 1. Set your production URL
export SITE_URL="https://docs.yourcompany.com"

# 2. Set the path (use "/" for root, or "/docs/" for subdirectory)
export BASE_URL="/"

# 3. Build and deploy
npm run build
```

**No code changes required.** Just set environment variables.

---

## Overview

Configure the Smart Humanoid documentation site for any deployment target using only environment variables. You don't need to know TypeScript or modify any code.

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SITE_URL` | Full canonical URL of the site | `http://localhost:3000` | No |
| `BASE_URL` | Path prefix for the site | `/` | No |

## Quick Start

### Local Development

No configuration needed. Just run:

```bash
npm start
```

The site will be available at `http://localhost:3000/`.

### Custom Domain Deployment

Set environment variables before building:

```bash
export SITE_URL="https://docs.example.com"
export BASE_URL="/"
npm run build
```

### Subdirectory Deployment

For deploying to a subdirectory (e.g., `/docs/`):

```bash
export SITE_URL="https://example.com"
export BASE_URL="/docs/"
npm run build
```

## Platform Examples

### GitHub Actions

```yaml
- name: Build site
  env:
    SITE_URL: https://docs.example.com
    BASE_URL: /
  run: npm run build
```

### Docker

```dockerfile
ENV SITE_URL=https://docs.example.com
ENV BASE_URL=/

RUN npm run build
```

### Netlify

In Netlify dashboard, set environment variables:
- `SITE_URL` = `https://your-site.netlify.app`
- `BASE_URL` = `/`

### Vercel

In Vercel dashboard, set environment variables:
- `SITE_URL` = `https://your-site.vercel.app`
- `BASE_URL` = `/`

## Using .env File (Local Development)

For convenience during local development, create a `.env` file:

```bash
# .env (do not commit this file)
SITE_URL=http://localhost:3000
BASE_URL=/
```

Note: The `.env` file is optional. Default values work for local development.

## Validation

The build will fail with a clear error message if:
- `SITE_URL` doesn't start with `http://` or `https://`
- `BASE_URL` doesn't start with `/`

## Troubleshooting

### Site shows wrong URL in metadata

Verify `SITE_URL` is set correctly:
```bash
echo $SITE_URL
```

### Assets not loading (404 errors)

Check `BASE_URL` matches your deployment path:
```bash
echo $BASE_URL
```

### Local development not working

Clear variables and use defaults:
```bash
unset SITE_URL
unset BASE_URL
npm start
```

## Reference

- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Implementation plan
- [data-model.md](./data-model.md) - Configuration entities
