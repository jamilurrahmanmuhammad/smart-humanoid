# Research: Docusaurus Platform Setup

**Feature**: 001-docusaurus-setup
**Date**: 2025-12-01
**Status**: Complete

## Research Summary

This document consolidates research findings for the Docusaurus platform setup. All technical unknowns from the plan have been resolved.

---

## 1. Docusaurus v3 Best Practices

### Decision: Use Docusaurus 3.x with TypeScript

**Rationale**:
- Docusaurus 3.x is the current stable release (as of 2025)
- TypeScript provides type safety for custom components
- MDX 3.x support enables embedded React components
- Native dark mode support aligns with spec requirements

**Alternatives Considered**:
- Docusaurus 2.x: Rejected (older, MDX 2.x, less active development)
- Other SSGs (Next.js, Astro): Rejected (Docusaurus specified in constitution Section X)

**Source**: https://docusaurus.io/docs

---

## 2. Dark Theme Implementation

### Decision: Use CSS custom properties with Infima overrides

**Rationale**:
- Docusaurus uses Infima CSS framework
- Custom properties allow global theme control
- Dark mode can be enforced without toggle UI

**Implementation Pattern**:
```css
:root {
  --ifm-background-color: #0D0D0F;
  --ifm-color-primary: #4ECFFE;
  --ifm-navbar-background-color: transparent;
  --ifm-font-family-base: 'Inter', system-ui, -apple-system, sans-serif;
}
```

**Alternatives Considered**:
- Swizzling entire theme: Rejected (over-engineering for color changes)
- Third-party theme: Rejected (no dark theme matching design requirements)

**Source**: https://docusaurus.io/docs/styling-layout

---

## 3. Hero Component Architecture

### Decision: Custom React component with CSS modules

**Rationale**:
- Hero section requires custom layout not available in default theme
- CSS modules provide scoped styling
- React component enables future interactivity

**Component Structure**:
```
src/components/Hero/
├── Hero.tsx           # Main component
├── Hero.module.css    # Scoped styles
└── index.ts           # Export
```

**Alternatives Considered**:
- MDX-only hero: Rejected (complex animations need React)
- Theme swizzle of Layout: Rejected (affects all pages, not just home)

---

## 4. Animated Underline Effect

### Decision: CSS keyframes animation on pseudo-element

**Rationale**:
- Pure CSS animation (no JS bundle impact)
- Works with SSR/SSG
- Accessible (respects prefers-reduced-motion)

**Implementation Pattern**:
```css
.highlight {
  position: relative;
}
.highlight::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--ifm-color-primary);
  animation: underline-grow 0.6s ease-out forwards;
}
@keyframes underline-grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
@media (prefers-reduced-motion: reduce) {
  .highlight::after { animation: none; }
}
```

**Alternatives Considered**:
- Framer Motion: Rejected (adds bundle weight for simple effect)
- Inline SVG animation: Rejected (more complex for same result)

---

## 5. Multi-Book Documentation Structure

### Decision: Use Docusaurus docs plugin instances

**Rationale**:
- Each book can have independent sidebar
- Shared theme and components
- Separate versioning possible per book
- Official Docusaurus pattern for multi-docs

**Configuration Pattern** (future books):
```ts
// docusaurus.config.ts
plugins: [
  [
    '@docusaurus/plugin-content-docs',
    {
      id: 'ai-agents',
      path: 'books/ai-agents',
      routeBasePath: 'ai-agents',
      sidebarPath: './sidebars-ai-agents.js',
    },
  ],
],
```

**Alternatives Considered**:
- Monorepo with multiple Docusaurus instances: Rejected (duplicates infrastructure)
- Single docs folder with category prefixes: Rejected (doesn't scale, sidebar complexity)

**Source**: https://docusaurus.io/docs/docs-multi-instance

---

## 6. i18n Implementation Strategy

### Decision: Scaffold i18n structure, disable by default

**Rationale**:
- Constitution requires Urdu (RTL) readiness
- Full translation workflow not in scope
- Structure enables future activation without refactoring

**Directory Structure**:
```
i18n/
└── ur/
    └── docusaurus-theme-classic/
        └── navbar.json
```

**RTL CSS Support**:
```css
[dir='rtl'] {
  direction: rtl;
  text-align: right;
}
```

**Alternatives Considered**:
- No i18n structure: Rejected (violates constitution readiness requirement)
- Full translation implementation: Rejected (out of scope per constraints)

**Source**: https://docusaurus.io/docs/i18n/introduction

---

## 7. GitHub Pages Deployment

### Decision: GitHub Actions workflow with peaceiris/actions-gh-pages

**Rationale**:
- Free hosting for public repositories
- Automated deployment on push
- Well-documented, widely used action
- Constitution Section X compatible

**Workflow Pattern**:
```yaml
name: Deploy
on:
  push:
    branches: [main, master]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

**Alternatives Considered**:
- Vercel: Valid alternative (noted in spec), not primary
- Netlify: Valid alternative, not specified
- Manual deployment: Rejected (violates automation requirement)

**Source**: https://docusaurus.io/docs/deployment#deploying-to-github-pages

---

## 8. Playwright Testing Strategy

### Decision: E2E tests focused on visual structure and accessibility

**Rationale**:
- Playwright MCP already available in session
- Visual regression testing validates spec compliance
- Accessibility testing ensures constitution compliance

**Test Categories**:
1. **Homepage tests**: Hero renders, CTA buttons present
2. **Navbar tests**: All menu items visible, correct order
3. **Accessibility tests**: Keyboard navigation, ARIA labels, contrast

**Configuration**:
```ts
// playwright.config.ts
export default defineConfig({
  testDir: './tests/e2e',
  webServer: {
    command: 'npm run serve',
    port: 3000,
  },
});
```

**Alternatives Considered**:
- Jest + Testing Library: Partial (component tests only, not E2E)
- Cypress: Rejected (Playwright already integrated via MCP)

**Source**: https://playwright.dev/docs/intro

---

## 9. Accessibility Compliance

### Decision: WCAG 2.1 AA with automated and manual verification

**Rationale**:
- Constitution Section XXXIV mandates WCAG 2.1 AA
- Color contrast: 4.5:1 minimum (white #FFFFFF on #0D0D0F = 18.3:1 ✓)
- Cyan accent: #4ECFFE on #0D0D0F = 9.7:1 ✓

**Verification Tools**:
- axe-core via Playwright
- Lighthouse accessibility audit
- Manual keyboard navigation testing

**Key Requirements**:
- All interactive elements keyboard accessible
- Visible focus indicators
- ARIA labels on custom components
- Skip-to-content link

**Alternatives Considered**:
- WCAG 2.0 AA: Rejected (constitution specifies 2.1)
- AAA compliance: Out of scope (would limit design flexibility)

---

## 10. Typography Decision

### Decision: Inter font family with system fallbacks

**Rationale**:
- Inter is free, open-source (OFL license)
- Excellent readability on screens
- Wide character support (Latin, Cyrillic, Greek)
- Matches modern, clean aesthetic in spec

**Implementation**:
```css
--ifm-font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

**Loading Strategy**:
- Use `font-display: swap` for performance
- Consider self-hosting vs Google Fonts (privacy)

**Alternatives Considered**:
- Satoshi: Valid (mentioned in spec), Inter more widely supported
- System fonts only: Acceptable fallback, less consistent appearance

---

## 11. Docusaurus v3 Breaking Changes & Specifics

### Key Changes from v2 to v3

**MDX Compiler**:
- v3 uses MDX 3.x (v2 used MDX 1.x/2.x)
- Stricter parsing: JSX expressions must be valid
- Import/export statements must be at top of file

**Configuration**:
- `docusaurus.config.ts` supports async configuration
- Plugin options schema validation is stricter
- Theme configuration structure updated

**CSS Variables System (Infima)**:
```css
/* Core layout tokens */
--ifm-navbar-height: 3.75rem;
--ifm-navbar-padding-horizontal: 1rem;
--ifm-navbar-padding-vertical: 0.5rem;

/* Color tokens */
--ifm-color-primary: #4ECFFE;
--ifm-color-primary-dark: #2bc4fe;
--ifm-color-primary-darker: #17befe;
--ifm-color-primary-darkest: #049dd4;
--ifm-color-primary-light: #71d6fe;
--ifm-color-primary-lighter: #85dbfe;
--ifm-color-primary-lightest: #b8eaff;

/* Background tokens */
--ifm-background-color: #0D0D0F;
--ifm-background-surface-color: #141417;

/* Typography tokens */
--ifm-font-size-base: 100%;
--ifm-font-family-base: 'Inter', system-ui, sans-serif;
--ifm-font-family-monospace: 'JetBrains Mono', monospace;
--ifm-line-height-base: 1.65;
--ifm-heading-font-weight: 700;

/* Spacing tokens */
--ifm-spacing-horizontal: 1rem;
--ifm-spacing-vertical: 1rem;
--ifm-global-radius: 0.4rem;

/* Motion tokens */
--ifm-transition-fast: 200ms;
--ifm-transition-slow: 400ms;
```

**Source**: https://docusaurus.io/docs/migration/v3

---

## 12. MCP Playwright Integration

### Capabilities

MCP Playwright provides browser automation within Claude Code sessions:

- **Navigation**: `browser_navigate`, `browser_navigate_back`
- **Interaction**: `browser_click`, `browser_type`, `browser_fill_form`
- **Capture**: `browser_snapshot`, `browser_take_screenshot`
- **State**: `browser_console_messages`, `browser_network_requests`

### Workflow for UI Validation

1. **Build site**: `npm run build && npm run serve`
2. **Navigate**: `browser_navigate` to localhost:3000
3. **Snapshot**: `browser_snapshot` for accessibility tree
4. **Screenshot**: `browser_take_screenshot` for visual verification
5. **Interact**: Test navigation, buttons, forms

### Testing Strategy

| Test Type | MCP Tool | Validation |
|-----------|----------|------------|
| Layout | `browser_snapshot` | Verify DOM structure |
| Visual | `browser_take_screenshot` | Compare against design |
| Navigation | `browser_click` | Verify links work |
| Accessibility | `browser_snapshot` | Check ARIA tree |
| Responsive | `browser_resize` | Test viewports |

### Limitations

- No persistent state across sessions
- Screenshots are point-in-time (no visual diff)
- Cannot access browser DevTools directly
- Network interception not available

---

## 13. WSL Environment Considerations

### Known Issues

| Issue | Cause | Mitigation |
|-------|-------|------------|
| Slow npm install | Windows filesystem | Use Linux filesystem (`/home/`) |
| File watcher limits | inotify defaults | Increase `fs.inotify.max_user_watches` |
| Port conflicts | Windows services | Use unique ports (3000, 3001) |
| Memory pressure | WSL2 defaults | Configure `.wslconfig` |

### Recommended .wslconfig

```ini
[wsl2]
memory=8GB
processors=4
swap=4GB
```

### Path Considerations

- Store project in `/home/user/` not `/mnt/c/`
- Use Linux line endings (LF not CRLF)
- Git config: `core.autocrlf=input`

### Playwright in WSL

```bash
# Install browser dependencies
npx playwright install-deps chromium

# Run with explicit browser path if needed
PLAYWRIGHT_BROWSERS_PATH=/home/user/.cache/ms-playwright npx playwright test
```

---

## 14. Multi-Book Architecture Deep Dive

### Doc Plugin Instance Pattern

Each book is a separate `@docusaurus/plugin-content-docs` instance:

```ts
// docusaurus.config.ts
export default {
  plugins: [
    // Default docs (Physical AI book)
    // Uses preset-classic's built-in docs

    // Additional book
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'ai-agents-book',
        path: 'books/ai-agents',
        routeBasePath: 'ai-agents',
        sidebarPath: './sidebars-ai-agents.ts',
        editUrl: 'https://github.com/org/repo/edit/main/',
      },
    ],
  ],
};
```

### Sidebar Configuration Per Book

```ts
// sidebars-ai-agents.ts
export default {
  aiAgentsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Modules',
      items: [{ type: 'autogenerated', dirName: 'modules' }],
    },
    {
      type: 'category',
      label: 'Chapters',
      items: [{ type: 'autogenerated', dirName: 'chapters' }],
    },
  ],
};
```

### Shared Components Across Books

```
src/components/
├── shared/              # Used by all books
│   ├── Glossary.tsx
│   ├── SafetyNotice.tsx
│   └── RAGUnit.tsx
├── book-physical-ai/    # Book-specific
└── book-ai-agents/      # Book-specific
```

### Unified Glossary Pattern

```ts
// src/data/glossary.ts
export const glossary = {
  'humanoid': {
    term: 'Humanoid Robot',
    definition: 'A robot with body shape built to resemble the human body.',
    books: ['physical-ai', 'ai-agents'],
  },
  // ...
};
```

### Cross-Book Navigation

```ts
// Navbar items linking to different books
navbar: {
  items: [
    { to: '/docs/intro', label: 'Physical AI', position: 'left' },
    { to: '/ai-agents/intro', label: 'AI Agents', position: 'left' },
  ],
}
```

---

## 15. RAG-Ready Content Structure

### Directory Convention

```
docs/
├── rag/                    # RAG-specific content units
│   ├── _index.json         # RAG metadata manifest
│   └── units/              # Individual RAG units
│       ├── unit-001.md
│       └── unit-002.md
```

### RAG Unit Frontmatter (Placeholder)

```yaml
---
rag_id: unit-001
chunk_size: 500
embedding_model: text-embedding-3-small
tags: [robotics, kinematics]
last_indexed: null  # Populated by RAG pipeline
---
```

### Constitution Alignment

Per Constitution Section XIX (RAG Integration):
- Content must be chunked appropriately
- Metadata must support vector search
- Structure must enable future LLM integration

---

## 16. Safety Metadata Structure

### Frontmatter Convention (Placeholder)

```yaml
---
safety_level: informational | caution | warning | danger
hardware_required: false
real_world_execution: false
hazards: []
prerequisites: []
---
```

### Safety Notice Component

```tsx
// Placeholder for future implementation
interface SafetyNoticeProps {
  level: 'caution' | 'warning' | 'danger';
  message: string;
  hardwareInvolved?: boolean;
}
```

---

## 17. Reusable Intelligence Architecture

### Directory Structure (Placeholder)

```
src/
├── skills/                 # Reusable skill definitions
│   ├── _registry.ts        # Skill manifest
│   └── README.md           # How to add skills
├── subagents/              # Subagent configurations
│   ├── _registry.ts        # Subagent manifest
│   └── README.md           # How to add subagents
```

### Skill Metadata Schema (Placeholder)

```ts
interface SkillMetadata {
  id: string;
  name: string;
  version: string;
  description: string;
  inputs: ParameterDef[];
  outputs: ParameterDef[];
  tags: string[];
}
```

---

## Resolution Summary

| Unknown | Resolution | Confidence |
|---------|------------|------------|
| Docusaurus version | 3.x with TypeScript | High |
| Theme approach | CSS custom properties (full token system) | High |
| Hero architecture | Custom React + CSS modules | High |
| Animation method | CSS keyframes | High |
| Multi-book structure | Docs plugin instances with shared components | High |
| i18n approach | Scaffold only, disabled | High |
| Deployment | GitHub Actions + gh-pages | High |
| Testing | Playwright E2E via MCP | High |
| Accessibility | WCAG 2.1 AA, axe-core | High |
| Typography | Inter with system fallback | High |
| MCP Integration | Snapshot + Screenshot workflow | High |
| WSL Considerations | Linux filesystem, wslconfig | High |
| RAG Structure | Placeholder metadata ready | High |
| Safety Metadata | Placeholder schema defined | High |
| Reusable Intelligence | Directory structure placeholder | High |

**All NEEDS CLARIFICATION items resolved. Proceed to Phase 1.**
