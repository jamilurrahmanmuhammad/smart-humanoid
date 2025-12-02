# Implementation Plan: Fix Chapter Navigation Order

**Branch**: `007-fix-chapter-nav-order` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-fix-chapter-nav-order/spec.md`

## Summary

Fix Docusaurus sidebar navigation ordering by correcting overlapping `sidebar_position` frontmatter values in chapter files. Chapter 2 variants currently have positions 3, 4, 5 which overlap with Chapter 1 (2, 3, 4). Update to ensure sequential, non-overlapping positions: Ch1 (2-4), Ch2 (5-7), Ch3 (8-10).

## Technical Context

**Language/Version**: Markdown (Docusaurus 3.x compatible)
**Primary Dependencies**: Docusaurus 3.x (existing)
**Storage**: N/A (file-based content)
**Testing**: Docusaurus build verification, visual inspection
**Target Platform**: GitHub Pages / Vercel (existing deployment)
**Project Type**: Documentation site
**Performance Goals**: N/A (no runtime impact)
**Constraints**: Must not break existing builds
**Scale/Scope**: 6 files to modify (Chapter 2 and Chapter 3 variants)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| XIII. Adaptive Content - Variant Strategy | ✅ PASS | Maintains three variants per chapter |
| XXXVI. Chapter Structure | ✅ PASS | Only modifying frontmatter, not content |
| XXXVII. Visual Standards | ✅ PASS | No visual changes |
| XXXVIII. Content Review Gates | ✅ PASS | Will verify with build |

**GATE RESULT**: ✅ All gates pass. Proceed to implementation.

## Project Structure

### Documentation (this feature)

```text
specs/007-fix-chapter-nav-order/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Files (to be modified)

```text
docs/module-1-robotic-nervous-system/
├── index.md                                    # Position 1 (OK - no change)
├── chapter-1-physical-ai-foundations-explorer.md  # Position 2 (OK)
├── chapter-1-physical-ai-foundations-builder.md   # Position 3 (OK)
├── chapter-1-physical-ai-foundations-engineer.md  # Position 4 (OK)
├── chapter-2-ros2-architecture-explorer.md     # Position 3→5 (FIX)
├── chapter-2-ros2-architecture-builder.md      # Position 4→6 (FIX)
├── chapter-2-ros2-architecture-engineer.md     # Position 5→7 (FIX)
├── chapter-3-urdf-modeling-explorer.md         # Position 6→8 (FIX)
├── chapter-3-urdf-modeling-builder.md          # Position 7→9 (FIX)
└── chapter-3-urdf-modeling-engineer.md         # Position 8→10 (FIX)
```

**Structure Decision**: No source code changes. Only YAML frontmatter updates in existing Markdown files.

## Complexity Tracking

No complexity violations. This is a minimal frontmatter fix.

## Implementation Approach

### Phase 0: Research (SKIPPED)

No research needed. The fix is straightforward:
- Root cause identified: overlapping `sidebar_position` values
- Solution clear: update to non-overlapping sequential values
- No external dependencies or unknowns

### Phase 1: Design (MINIMAL)

**Position Formula**: `position = (chapter_number - 1) * 3 + variant_offset + 1`

| Chapter | Variant | Offset | Formula | Position |
|---------|---------|--------|---------|----------|
| 1 | Explorer | 1 | (1-1)*3 + 1 + 1 | 2 |
| 1 | Builder | 2 | (1-1)*3 + 2 + 1 | 3 |
| 1 | Engineer | 3 | (1-1)*3 + 3 + 1 | 4 |
| 2 | Explorer | 1 | (2-1)*3 + 1 + 1 | 5 |
| 2 | Builder | 2 | (2-1)*3 + 2 + 1 | 6 |
| 2 | Engineer | 3 | (2-1)*3 + 3 + 1 | 7 |
| 3 | Explorer | 1 | (3-1)*3 + 1 + 1 | 8 |
| 3 | Builder | 2 | (3-1)*3 + 2 + 1 | 9 |
| 3 | Engineer | 3 | (3-1)*3 + 3 + 1 | 10 |

### Changes Required

| File | Current Position | New Position |
|------|------------------|--------------|
| chapter-2-ros2-architecture-explorer.md | 3 | 5 |
| chapter-2-ros2-architecture-builder.md | 4 | 6 |
| chapter-2-ros2-architecture-engineer.md | 5 | 7 |
| chapter-3-urdf-modeling-explorer.md | 6 | 8 |
| chapter-3-urdf-modeling-builder.md | 7 | 9 |
| chapter-3-urdf-modeling-engineer.md | 8 | 10 |

### Validation Steps

1. Update all 6 files with correct `sidebar_position` values
2. Run `npm run build` to verify Docusaurus builds successfully
3. Run `npm run serve` and visually confirm navigation order
4. Verify: Ch1 (Explorer, Builder, Engineer) → Ch2 (Explorer, Builder, Engineer) → Ch3 (Explorer, Builder, Engineer)

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Typo in position value | Low | Low | Verify with build |
| Break existing links | None | N/A | sidebar_position doesn't affect URLs |
| Conflict with future chapters | Low | Low | Convention documented in spec |

## Dependencies

None. This is a standalone fix.

## Artifacts Not Required

Given the simplicity of this fix, the following Phase 1 artifacts are NOT required:

- **research.md**: No research needed - problem and solution are clear
- **data-model.md**: No data model - this is a frontmatter fix
- **contracts/**: No API contracts - this is documentation only
- **quickstart.md**: No quickstart - single-purpose fix

## Next Steps

Run `/sp.tasks` to generate the task breakdown, then `/sp.implement` to execute the fix.
