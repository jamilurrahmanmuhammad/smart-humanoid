# Implementation Plan: Docusaurus Platform Setup

**Branch**: `001-docusaurus-setup` | **Date**: 2025-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-docusaurus-setup/spec.md`

## Summary

Set up Docusaurus v3 as platform-level infrastructure for the multi-book educational ecosystem. The implementation creates a professional landing page with dark theme (#0D0D0F), cyan accents (#4ECFFE), modern hero section, and scaffolded documentation structure ready for book content. The platform will be constitution-compliant (WCAG 2.1 AA, i18n-ready, RTL-ready).

## Architecture Philosophy

> **"Minimal now, frictionless later"** - Start with pure Docusaurus simplicity. Design extension points so future features plug in like "connecting a wire to a socket."

**Core Principles**:
1. **Open Source Only** - Zero licensing costs, no vendor lock-in
2. **Open Standards** - Interfaces follow industry patterns (OpenAI-compatible, OAuth2, REST)
3. **Configuration-Driven** - Admin adds API keys at deployment, not code changes
4. **Pluggable Everything** - Auth, LLM, Vector DB, Hosting all optional plugins
5. **Constitution-Aligned** - Architecture supports all future requirements without re-design

## Technical Context

**Language/Version**: TypeScript 5.x, Node.js 18+
**Primary Dependencies**: Docusaurus 3.x, React 18.x, MDX 3.x (all MIT licensed)
**Storage**: Static files (Markdown/MDX) - database pluggable later
**Testing**: Playwright for E2E/visual testing
**Target Platform**: Local dev / GitHub Pages (other hosting pluggable)
**Project Type**: Static site with plugin-ready service architecture
**Performance Goals**: Page load < 3 seconds, build < 60 seconds
**Constraints**: Zero build warnings, WCAG 2.1 AA, responsive 320px-1920px, zero licensing costs

## Pluggable Architecture Design

### What Ships Now (Minimal)

| Component | Implementation | Complexity |
|-----------|----------------|------------|
| Site Framework | Docusaurus 3.x | Simple |
| Styling | CSS custom properties | Simple |
| Components | React (Hero, Navbar, placeholders) | Simple |
| Content | Static MDX files | Simple |
| Deployment | Manual or GitHub Pages | Simple |

### What's Plug-Ready (Zero Code Now, Easy Later)

| Feature | Interface Ready | Default (Now) | Plugs Into (Later) |
|---------|-----------------|---------------|-------------------|
| **Auth** | `IAuthProvider` | Disabled | Better-Auth, Lucia, NextAuth |
| **LLM** | `ILLMProvider` (OpenAI-compatible) | Disabled | Ollama, OpenAI, Anthropic, Groq |
| **Vector Search** | `IVectorProvider` | Disabled | pgvector, Qdrant, Pinecone |
| **Database** | `IDataProvider` | localStorage mock | PostgreSQL, SQLite, Neon |
| **Analytics** | `IAnalyticsProvider` | Console only | Plausible, PostHog, custom |
| **Hosting** | Standard build output | Local/GH Pages | Vercel, Cloudflare, self-hosted |

### How Plugins Work

**1. Environment-Based Configuration**

All optional features are controlled via environment variables set at deployment time. By default, all plugins are disabled. The admin copies the environment template file and enables features by setting flags to true and providing necessary configuration values (API endpoints, keys, etc.).

**2. Provider Interface Pattern**

Each pluggable feature has a defined interface (contract) that any implementation must follow. The system includes a factory function that checks the environment configuration and returns the appropriate provider, or null if the feature is disabled.

**3. Feature Detection in Components**

UI components check if a feature is enabled before rendering. If a provider returns null (disabled), the component renders a placeholder. When enabled, it uses the active provider automatically.

### Open Standards Compliance

| Feature | Standard | Why |
|---------|----------|-----|
| LLM API | OpenAI Chat Completions format | Works with Ollama, LiteLLM, vLLM, any compatible |
| Auth | OAuth 2.0 / OIDC | Better-Auth, Lucia, NextAuth all support |
| Vector API | REST with standard embedding format | pgvector, Qdrant, Chroma all compatible |
| Content | MDX 3.x | Industry standard, Docusaurus native |
| Styling | CSS custom properties | Framework agnostic |

### Directory Structure for Plugins

The source directory will include a providers folder containing subdirectories for each plugin type (auth, llm, vector, data). Each subdirectory contains an interface definition file and an index file that returns either the active provider or null.

A hooks folder will contain React hooks for accessing providers, returning null when features are disabled.

A config folder will contain feature flag definitions and provider configuration.

### Adding a Plugin Later

To enable a new plugin:

1. Create a provider implementation that fulfills the interface contract
2. Register the implementation in the provider factory
3. Set the appropriate environment variables
4. Components automatically detect and use the new provider

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | How Validated |
|-----------|--------|---------------|
| **X. Content Delivery** (Docusaurus 3.x) | ✅ PASS | Build succeeds with Docusaurus 3.x |
| **XII. Identity & Personalization** | ✅ PASS | Personalize button visible in navbar, disabled state |
| **XIII. Adaptive Content** | ✅ PASS | i18n directory exists with Urdu placeholder |
| **XIV. Infrastructure Principles** | ✅ PASS | All dependencies MIT/Apache licensed, no secrets in code |
| **XIX. RAG Integration** | ✅ PASS | /docs/rag/ directory exists with manifest placeholder |
| **XXI. Translation Governance** | ✅ PASS | /i18n/ur/ scaffolded, RTL CSS prepared |
| **XXII. Reusable Intelligence** | ✅ PASS | /src/skills/ and /src/subagents/ directories exist |
| **XXIII. Urdu Linguistics QA** | ✅ PASS | RTL direction CSS attribute ready |
| **XXXI. UI Component Standards** | ✅ PASS | Personalize/Translate buttons present as placeholders |
| **XXXIV. Inclusive Design** | ✅ PASS | axe-core audit passes, keyboard navigation works |
| **XXXV. Safety Standards** | ✅ PASS | Frontmatter schema supports safety metadata fields |
| **XXXVII. Visual Standards** | ✅ PASS | Alt text on images, code syntax highlighting enabled |

### Constitution Validation Process

During implementation, each principle will be validated as follows:

**Accessibility (XXXIV)**:
- Run axe-core accessibility audit via Playwright
- Verify all interactive elements are keyboard reachable
- Check color contrast ratios meet WCAG 2.1 AA (4.5:1 minimum)
- Confirm visible focus indicators on all focusable elements

**Multi-Book Readiness (X)**:
- Verify docs plugin configuration supports multiple instances
- Test adding a second book directory without modifying core config
- Confirm sidebars generate independently per book

**Translation Readiness (XXI, XXIII)**:
- Verify i18n directory structure matches Docusaurus conventions
- Test RTL CSS applies correctly when direction attribute is set
- Confirm navbar translation file placeholder exists

**RAG Readiness (XIX)**:
- Verify /docs/rag/ directory exists
- Confirm manifest placeholder file is present
- Check frontmatter schema documentation includes RAG metadata fields

**Safety Metadata (XXXV)**:
- Verify frontmatter documentation includes safety fields
- Confirm intro.md template shows safety metadata placeholders

**Reusable Intelligence (XXII)**:
- Verify /src/skills/ directory exists with README
- Verify /src/subagents/ directory exists with README
- Confirm placeholder registry files are present

**Gate Result**: ✅ ALL GATES PASS - Proceed to Phase 0

---

## MCP Playwright Testing Strategy

MCP Playwright will be used throughout implementation for UI validation. This section defines the testing approach.

### Testing Workflow

1. **After each UI stage completes**: Run browser snapshot to verify DOM structure
2. **After styling changes**: Take screenshot for visual verification
3. **After adding interactive elements**: Test keyboard navigation and clicks
4. **Before deployment**: Full validation pass on all acceptance criteria

### Test Categories

| Category | What to Test | MCP Tools Used |
|----------|--------------|----------------|
| **Layout** | Hero section dimensions, flex layout, responsive breakpoints | browser_snapshot, browser_resize |
| **Navigation** | All navbar items present, links work, hover states | browser_click, browser_snapshot |
| **Accessibility** | ARIA tree structure, focusable elements, keyboard flow | browser_snapshot (accessibility tree) |
| **Visual** | Dark theme colors, accent colors, typography | browser_take_screenshot |
| **Interaction** | Button clicks, menu hovers, placeholder states | browser_click, browser_hover |

### Validation Checkpoints

**Stage 1 (Bootstrap)**: Verify Docusaurus serves on localhost, dark background visible
**Stage 2 (Hero)**: Screenshot hero section, verify flex layout, check headline animation
**Stage 3 (Navbar)**: Snapshot accessibility tree, verify all 5 navbar elements present
**Stage 4 (Docs)**: Navigate to /docs, verify sidebar renders, check folder structure
**Stage 8 (Deployment)**: Full validation pass on deployed URL

### Responsive Testing

Test at three viewport sizes:
- Desktop: 1920x1080
- Tablet: 768x1024
- Mobile: 375x667

Use browser_resize to switch viewports, then browser_snapshot to verify layout adapts correctly.

## Project Structure

### Documentation (this feature)

```text
specs/001-docusaurus-setup/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (component interfaces)
├── checklists/          # Quality validation
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Docusaurus Platform Structure (Plugin-Ready)
/
├── docusaurus.config.ts     # Main configuration
├── sidebars.ts              # Sidebar configuration
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
├── .env.example             # Environment template (admin copies to .env.local)
│
├── src/
│   ├── components/          # UI Components
│   │   ├── Hero/
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   └── placeholders/    # Future feature placeholders
│   │       ├── PersonalizeButton.tsx
│   │       ├── TranslateButton.tsx
│   │       └── TryWithAI.tsx
│   │
│   ├── providers/           # Plugin interfaces (MINIMAL NOW)
│   │   ├── index.ts         # Provider exports
│   │   ├── types.ts         # Shared TypeScript interfaces
│   │   └── README.md        # How to add providers
│   │
│   ├── hooks/               # React hooks
│   │   └── useFeatureFlag.ts
│   │
│   ├── config/
│   │   └── features.ts      # Feature flags from env
│   │
│   ├── css/
│   │   └── custom.css       # Theme overrides
│   │
│   └── pages/
│       └── index.tsx        # Homepage with Hero
│
├── docs/                    # Book content (Physical AI)
│   ├── intro.md
│   ├── modules/
│   ├── chapters/
│   ├── rag/
│   └── assets/
│
├── i18n/                    # i18n scaffold (disabled)
│   └── ur/
│
├── static/
│   └── img/
│
└── .github/
    └── workflows/
        └── deploy.yml       # GitHub Pages (optional)
```

**Structure Decision**: Minimal Docusaurus at root with lightweight provider pattern. Providers are just interfaces now (no implementations). Future features add implementations without changing structure.

## Implementation Stages

> **Philosophy**: Each stage is independently valuable. Stop at any stage and have a working site.

### Stage 1: Bootstrap Docusaurus (CORE)

**Purpose**: Get a working Docusaurus site with dark theme

**Steps**:
1. Verify Node.js ≥ 18, npm available
2. Run `npx create-docusaurus@latest . classic --typescript`
3. Remove default blog content
4. Configure `docusaurus.config.ts`:
   - Title: "Smart Humanoid"
   - Tagline: "Build robots that understand the physical world"
   - Dark mode default, switch disabled
5. Create `src/css/custom.css` with theme variables:
   - `--ifm-background-color: #0D0D0F`
   - `--ifm-color-primary: #4ECFFE`

**Validation**: `npm run build` succeeds, dark theme visible
**Deliverable**: Working Docusaurus site with Smart Humanoid colors

---

### Stage 2: Hero & Homepage (CORE)

**Purpose**: Create the branded landing page

**Steps**:
1. Create `src/components/Hero/` component:
   - Platform label (uppercase, letter-spacing)
   - Headline with animated "understand" highlight
   - Subheading + two CTA buttons
   - Diagram placeholder (right side)
2. Create `src/pages/index.tsx` using Hero
3. Add animated underline CSS keyframes

**Validation**: Homepage matches design specification
**Deliverable**: Professional landing page

---

### Stage 3: Navbar & Navigation (CORE)

**Purpose**: Site-wide navigation

**Steps**:
1. Configure navbar in `docusaurus.config.ts`:
   - "Learn Free" → /docs/intro
   - "Labs" → disabled placeholder
   - "Personalize" → disabled placeholder
   - Search box placeholder
   - GitHub link icon
2. Style navbar transparent over dark background

**Validation**: All 5 navbar elements visible
**Deliverable**: Complete navigation

---

### Stage 4: Documentation Structure (CORE)

**Purpose**: Book content scaffold

**Steps**:
1. Create docs structure:
   ```
   docs/intro.md
   docs/modules/.gitkeep
   docs/chapters/.gitkeep
   docs/rag/.gitkeep
   docs/assets/.gitkeep
   ```
2. Configure sidebar auto-generation
3. Write placeholder intro.md

**Validation**: /docs shows sidebar with hierarchy
**Deliverable**: Ready for book content

---

### Stage 5: Plugin Architecture (ARCHITECTURE)

**Purpose**: Enable frictionless future extensions

**Steps**:
1. Create `.env.example` with all feature flags (disabled):
   ```
   ENABLE_AUTH=false
   ENABLE_LLM=false
   ENABLE_VECTOR_SEARCH=false
   ENABLE_ANALYTICS=false
   ```
2. Create `src/config/features.ts` reading from env
3. Create `src/providers/types.ts` with interfaces:
   - `IAuthProvider`
   - `ILLMProvider` (OpenAI-compatible)
   - `IVectorProvider`
   - `IDataProvider`
4. Create `src/providers/README.md` documenting how to add providers
5. Create `src/hooks/useFeatureFlag.ts`

**Validation**: Interfaces compile, README is clear
**Deliverable**: Plugin-ready architecture

---

### Stage 6: Placeholder Components (UI)

**Purpose**: UI elements for future features

**Steps**:
1. Create `src/components/placeholders/`:
   - `PersonalizeButton.tsx` (disabled, styled)
   - `TranslateButton.tsx` (disabled, styled)
   - `TryWithAI.tsx` (disabled, styled)
2. Add ARIA labels for accessibility
3. Components show "Coming Soon" state

**Validation**: Components render without errors
**Deliverable**: Professional placeholders

---

### Stage 7: i18n Scaffold (OPTIONAL)

**Purpose**: Prepare for Urdu translation

**Steps**:
1. Create `i18n/ur/` directory structure
2. Add RTL-ready CSS (disabled by default)
3. Configure i18n in docusaurus.config.ts (disabled)

**Validation**: Build succeeds with i18n config
**Deliverable**: Translation-ready structure

---

### Stage 8: Deployment Workflow (OPTIONAL)

**Purpose**: GitHub Pages deployment

**Steps**:
1. Create `.github/workflows/deploy.yml`
2. Configure for GitHub Pages
3. Set `baseUrl` and `url` in config

**Validation**: Push triggers successful deployment
**Deliverable**: Automated deployment

---

### Stage 9: Testing Setup (OPTIONAL)

**Purpose**: Automated UI verification

**Steps**:
1. Install Playwright: `npm install -D @playwright/test`
2. Create basic test files for homepage, navbar
3. Configure test scripts

**Validation**: `npm run test` passes
**Deliverable**: Test infrastructure

---

### Stage 10: Final Validation

**Checklist**:
- [ ] Dark theme (#0D0D0F) working
- [ ] Cyan accents (#4ECFFE) applied
- [ ] Hero section renders correctly
- [ ] Navbar has all 5 elements
- [ ] Docs structure exists
- [ ] Plugin interfaces defined
- [ ] Feature flags in .env.example
- [ ] Zero build warnings
- [ ] Responsive layout works

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| WSL2 memory pressure | Medium | Build fails | Configure .wslconfig memory limits |
| Playwright browser missing | Low | Tests fail | Run `npx playwright install chromium` |
| Docusaurus version mismatch | Low | Breaking changes | Pin exact version in package.json |
| Sidebar not generating | Low | Navigation broken | Verify folder naming conventions |
| RTL CSS conflicts | Low | Urdu layout issues | Test RTL separately before enabling |

## Dependencies & External Resources

**Documentation**:
- Docusaurus: https://docusaurus.io/docs
- Docusaurus Installation: https://docusaurus.io/docs/installation
- Docusaurus Deployment: https://docusaurus.io/docs/deployment
- Playwright: https://playwright.dev/docs/intro

**Design Reference**:
- Professional dark theme with hero section
- Colors: #0D0D0F (background), #4ECFFE (accent)
- Typography: Inter or system sans-serif

## Complexity Tracking

> No violations requiring justification. Design follows minimal complexity principles.

| Item | Complexity | Justification |
|------|------------|---------------|
| Single Docusaurus project | Simple | Platform-level, shared across books |
| Custom Hero component | Moderate | Required for spec compliance |
| Playwright tests | Moderate | Required for automated validation |
| i18n scaffold | Simple | Prepare-only, not activated |

## Out of Scope

Per specification constraints:
- Real book content (only scaffolds)
- AI backend (RAG, FastAPI, Neon)
- Branding graphics (placeholder only)
- Simulation content
- Subagent implementations
- Analytics integration
- Authentication implementation

These belong to future feature specifications.

---

**Plan Version**: 1.0.0
**Plan Author**: Claude Code via /sp.plan
**Next Step**: `/sp.tasks` to generate actionable task list
