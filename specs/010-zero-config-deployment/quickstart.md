# Quickstart: Zero-Config Platform Deployment

**Feature**: 010-zero-config-deployment
**Audience**: DevOps Engineers, Developers deploying the site

## Overview

This project supports zero-configuration deployment to any standards-compliant hosting platform. Simply import the repository - no manual configuration required.

## Deployment Methods

### Method 1: One-Click Import (Recommended)

1. Go to your hosting platform (Vercel, Netlify, Cloudflare Pages, etc.)
2. Import the repository by URL: `https://github.com/jamilurrahmanmuhammad/smart-humanoid`
3. Click Deploy - that's it!

The platform will automatically:
- Detect Docusaurus as the framework
- Use `npm run build` as the build command
- Use `build/` as the output directory
- Use Node.js 20+ as specified in `engines`

### Method 2: CLI Deployment

```bash
# Clone the repository
git clone https://github.com/jamilurrahmanmuhammad/smart-humanoid
cd smart-humanoid

# Install dependencies
npm install

# Build for production
npm run build

# The build/ directory contains the static site
# Upload this directory to any static hosting service
```

### Method 3: Custom URL Configuration

If your platform requires specific URL configuration:

```bash
# Set environment variables before building
SITE_URL=https://your-domain.com BASE_URL=/ npm run build
```

Or for subdirectory deployment:

```bash
SITE_URL=https://your-domain.com BASE_URL=/docs/ npm run build
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| SITE_URL | `http://localhost:3000` | Full URL of deployed site |
| BASE_URL | `/` | Base path (use `/subdir/` for subdirectory) |
| CI | - | Automatically set by platforms; enables CI mode |

## How It Works

### Industry-Standard Detection

The project uses only industry-standard conventions that all platforms recognize:

1. **package.json** contains:
   - `engines.node: ">=20.0"` - specifies Node.js version
   - `scripts.build: "docusaurus build"` - standard build command
   - `scripts.start: "docusaurus start"` - development command

2. **Build output** goes to `build/` directory (Docusaurus default)

3. **CI detection** via `CI=true` environment variable (set by all platforms)

### No Platform-Specific Files

This project intentionally avoids:
- `vercel.json`
- `netlify.toml`
- `render.yaml`
- Any other platform-specific configuration

This ensures the repository works with ANY standards-compliant platform.

## Local Development

```bash
# Start development server
npm start

# Runs at http://localhost:3000 by default
```

## Testing Deployment Locally

```bash
# Build the site
npm run build

# Serve the build locally
npm run serve

# Or simulate CI environment
CI=true npm run build
```

## Troubleshooting

### Build fails with "Invalid URL"

Ensure SITE_URL starts with `http://` or `https://`:
```bash
# Correct
SITE_URL=https://example.com npm run build

# Incorrect - will fail
SITE_URL=example.com npm run build
```

### Links broken on deployed site

Ensure BASE_URL starts with `/` and ends with `/` for subdirectories:
```bash
# For root deployment
BASE_URL=/ npm run build

# For subdirectory
BASE_URL=/docs/ npm run build
```

### Platform doesn't detect framework

Verify `package.json` contains:
```json
{
  "engines": {
    "node": ">=20.0"
  },
  "scripts": {
    "build": "docusaurus build",
    "start": "docusaurus start"
  }
}
```

## Platform-Specific Notes

### Any Platform

Should work out-of-the-box. If not:
1. Set build command to `npm run build`
2. Set output directory to `build`
3. Set Node.js version to 20+

### GitHub Pages

For GitHub Pages with custom domain or project pages:
```bash
SITE_URL=https://username.github.io BASE_URL=/repo-name/ npm run build
```

### Custom Servers

Simply upload the contents of the `build/` directory to your web server's document root.

## Verification Checklist

- [ ] Site loads at deployed URL
- [ ] All navigation links work
- [ ] All images and assets load
- [ ] No console errors about broken resources
- [ ] Search (if implemented) functions correctly
