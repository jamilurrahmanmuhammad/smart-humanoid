# Implementation Plan: Hierarchical Documentation Structure

**Branch**: `003-docs-structure-user-story-3` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-docs-structure-user-story-3/spec.md`

## Summary

Restructure the Smart Humanoid documentation from a flat sibling structure (`docs/modules/`, `docs/chapters/`) to a hierarchical structure where chapters are nested inside modules. This enables progressive learning paths with modules as expandable sidebar categories containing their child chapters.

## Technical Context

**Language/Version**: TypeScript (Docusaurus 3.x)
**Primary Dependencies**: Docusaurus 3.x, React 18
**Storage**: Filesystem (Markdown files with frontmatter)
**Testing**: Playwright E2E tests
**Target Platform**: Static web (GitHub Pages)
**Project Type**: Documentation platform (Docusaurus)
**Performance Goals**: Build <60s, page load <3s
**Constraints**: Use native Docusaurus sidebar generation, no custom plugins
**Scale/Scope**: ~10 documentation files, 4 modules planned

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| X. Content Delivery (Docusaurus 3.x) | ✅ Pass | Using Docusaurus native features |
| XXXV. Domain Structure (Module hierarchy) | ✅ Pass | Implementing constitution's 4-module structure |
| XXXVI. Chapter Structure | ✅ Pass | Chapters as files within module directories |
| XXXIV. Inclusive Design (Accessibility) | ✅ Pass | Sidebar remains keyboard accessible |
| XIV. Infrastructure (No hardcoded secrets) | ✅ Pass | No secrets involved |

**Gate Status**: ✅ PASSED - No violations

## Project Structure

### Documentation (this feature)

```text
specs/003-docs-structure-user-story-3/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
docs/
├── intro.md                              # Welcome page (unchanged)
├── module-1-robotic-nervous-system/      # Module 1 (new structure)
│   ├── _category_.json                   # Sidebar config: position 2, label
│   ├── index.md                          # Module landing page
│   └── [chapter files]                   # Future chapters
├── module-2-digital-twin/                # Module 2 (new structure)
│   ├── _category_.json
│   ├── index.md
│   └── [chapter files]
├── module-3-ai-robot-brain/              # Module 3 (new structure)
│   ├── _category_.json
│   ├── index.md
│   └── [chapter files]
├── module-4-vision-language-action/      # Module 4 (new structure)
│   ├── _category_.json
│   ├── index.md
│   └── [chapter files]
├── rag/                                  # AI assistant content (unchanged)
│   └── .gitkeep
└── assets/                               # Documentation assets (unchanged)
    └── .gitkeep

tests/e2e/
├── homepage.spec.ts                      # 6 tests (unchanged)
├── navigation.spec.ts                    # 7 tests (unchanged)
└── docs.spec.ts                          # 4 tests (update for new structure)
```

**Structure Decision**: Docusaurus documentation platform with hierarchical module > chapter organization. Each module is a directory with `_category_.json` for sidebar configuration and `index.md` as landing page. Chapters are markdown files within module directories.

## Migration Plan

### Current State
```text
docs/
├── intro.md
├── modules/
│   ├── _category_.json
│   └── index.md
├── chapters/
│   ├── _category_.json
│   └── index.md
├── rag/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

### Target State
```text
docs/
├── intro.md
├── module-1-robotic-nervous-system/
│   ├── _category_.json
│   └── index.md
├── module-2-digital-twin/
│   ├── _category_.json
│   └── index.md
├── module-3-ai-robot-brain/
│   ├── _category_.json
│   └── index.md
├── module-4-vision-language-action/
│   ├── _category_.json
│   └── index.md
├── rag/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

### Migration Steps

1. Create 4 module directories with proper naming convention
2. Create `_category_.json` for each module with position and label
3. Create `index.md` for each module as landing page
4. Remove old `docs/modules/` directory
5. Remove old `docs/chapters/` directory
6. Update E2E tests to verify new sidebar structure
7. Rebuild and verify all 17 tests pass

## Complexity Tracking

> No constitution violations - no complexity justification needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | - | - |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing E2E tests | High | Update test selectors to match new structure |
| Sidebar not rendering correctly | Medium | Test with Playwright after each change |
| Build failures | Medium | Incremental changes with build verification |

## Definition of Done

- [ ] 4 module directories created with `_category_.json` and `index.md`
- [ ] Old `modules/` and `chapters/` directories removed
- [ ] Sidebar displays modules as expandable categories
- [ ] Chapters appear nested under modules in sidebar
- [ ] All 17 E2E tests pass
- [ ] Build completes with zero errors/warnings
