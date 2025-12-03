# ADR-0001: Zero-Config Deployment Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-03
- **Feature:** 010-zero-config-deployment
- **Context:** The Smart Humanoid documentation site needs to support deployment to any standards-compliant hosting platform (Vercel, Netlify, Cloudflare Pages, GitHub Pages, etc.) without requiring platform-specific configuration files. The goal is maximum portability and zero-friction repository imports.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects all future deployments
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - platform-specific vs industry-standard
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects config, CI, package.json, build process
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will rely solely on industry-standard Node.js conventions for deployment configuration:

- **CI Detection:** Use `CI=true` environment variable (set automatically by all major CI/CD platforms)
- **Configuration Files:** No platform-specific files (vercel.json, netlify.toml, render.yaml, etc.)
- **Package.json Standards:**
  - `engines.node: ">=20.0"` - specifies Node.js version
  - `scripts.build: "docusaurus build"` - standard build command
  - `scripts.start: "docusaurus start"` - standard dev command
- **Build Output:** `build/` directory (Docusaurus default, widely recognized)
- **URL Configuration:** Environment variables `SITE_URL` and `BASE_URL` (from feature 009)

## Consequences

### Positive

- **Maximum portability:** Repository works with any platform that follows Node.js conventions
- **Zero vendor lock-in:** No coupling to specific hosting providers
- **Simplified maintenance:** One configuration approach for all environments
- **Faster onboarding:** New team members don't need to learn platform-specific config
- **Future-proof:** Standards-compliant approach adapts to new platforms automatically

### Negative

- **Limited platform optimizations:** Cannot use platform-specific features (Vercel Edge Functions, Netlify redirects, etc.)
- **Manual URL configuration:** Some platforms may require manual SITE_URL/BASE_URL setup
- **No advanced caching rules:** Platform-specific caching headers require manual configuration
- **Debugging complexity:** Fewer platform-specific logging/debugging options

## Alternatives Considered

**Alternative A: Platform-Specific Configuration Files**
- Approach: Create vercel.json, netlify.toml, etc. for each target platform
- Pros: Platform-specific optimizations, better integration, automatic configuration
- Cons: Maintenance burden, vendor lock-in, config drift between platforms
- Why rejected: User requirement for industry-standard only; maintenance overhead for multi-platform support

**Alternative B: Hybrid Approach**
- Approach: Industry-standard defaults with optional platform-specific overrides
- Pros: Best of both worlds, gradual adoption
- Cons: Complexity, unclear precedence, testing burden
- Why rejected: Added complexity without clear benefit for documentation site use case

**Alternative C: Docker-Based Deployment**
- Approach: Containerize the build and deploy via Docker
- Pros: Maximum consistency, works anywhere
- Cons: Overkill for static site, slower builds, more infrastructure
- Why rejected: Unnecessary complexity for static documentation site

## References

- Feature Spec: [specs/010-zero-config-deployment/spec.md](../../specs/010-zero-config-deployment/spec.md)
- Implementation Plan: [specs/010-zero-config-deployment/plan.md](../../specs/010-zero-config-deployment/plan.md)
- Research: [specs/010-zero-config-deployment/research.md](../../specs/010-zero-config-deployment/research.md)
- Related ADRs: None (first ADR)
- Evaluator Evidence: N/A (architectural decision from planning phase)
