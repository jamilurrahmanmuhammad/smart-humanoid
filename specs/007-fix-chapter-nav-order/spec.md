# Feature Specification: Fix Chapter Navigation Order

**Feature Branch**: `007-fix-chapter-nav-order`
**Created**: 2025-12-02
**Status**: Draft
**Input**: User description: "I can see that the sequence of the chapters are a little wrong in the navigation bar. Modify the first feature which is docusaurus setup such that all the chapter variants should be in the sequence and should not mix the variants of different chapters in the list."

## Problem Statement

The Docusaurus sidebar navigation currently displays chapters in an incorrect order. Chapter variants (Explorer, Builder, Engineer) from different chapters are interleaved instead of being grouped by chapter. This happens because the `sidebar_position` frontmatter values overlap between chapters.

**Current State**:
- Chapter 1 variants: sidebar_position 2, 3, 4
- Chapter 2 variants: sidebar_position 3, 4, 5 (overlaps with Ch1!)
- Chapter 3 variants: sidebar_position 6, 7, 8

**Desired State**:
- Chapter 1 variants: sidebar_position 2, 3, 4
- Chapter 2 variants: sidebar_position 5, 6, 7
- Chapter 3 variants: sidebar_position 8, 9, 10
- (Module index remains at position 1)

## User Scenarios & Testing

### User Story 1 - Correct Navigation Order (Priority: P1)

A reader navigating Module 1 content sees all Chapter 1 variants grouped together, followed by all Chapter 2 variants, then all Chapter 3 variants—not interleaved.

**Why this priority**: This is the core functionality fix. Without proper ordering, users cannot navigate content logically.

**Independent Test**: Open the Docusaurus site and verify the Module 1 sidebar shows chapters in sequence: Ch1 Explorer, Ch1 Builder, Ch1 Engineer, Ch2 Explorer, Ch2 Builder, Ch2 Engineer, Ch3 Explorer, Ch3 Builder, Ch3 Engineer.

**Acceptance Scenarios**:

1. **Given** the Docusaurus site is running, **When** a user views the Module 1 sidebar, **Then** all Chapter 1 variants appear before any Chapter 2 variants
2. **Given** the sidebar displays chapters, **When** a user scans the navigation, **Then** each chapter's three variants (Explorer, Builder, Engineer) are consecutive
3. **Given** Chapter 2 variants, **When** comparing sidebar position values, **Then** all Chapter 2 positions are higher than all Chapter 1 positions

---

### Edge Cases

- What happens if a new chapter is added? The sidebar positions should follow the pattern: (chapter_number - 1) * 3 + variant_offset + 1, where variant_offset is 1 for Explorer, 2 for Builder, 3 for Engineer.
- What happens if the index.md position conflicts? The index.md should always remain at position 1.

## Requirements

### Functional Requirements

- **FR-001**: System MUST display Module 1 index as the first navigation item (sidebar_position: 1)
- **FR-002**: System MUST display Chapter 1 Explorer at sidebar_position 2
- **FR-003**: System MUST display Chapter 1 Builder at sidebar_position 3
- **FR-004**: System MUST display Chapter 1 Engineer at sidebar_position 4
- **FR-005**: System MUST display Chapter 2 Explorer at sidebar_position 5
- **FR-006**: System MUST display Chapter 2 Builder at sidebar_position 6
- **FR-007**: System MUST display Chapter 2 Engineer at sidebar_position 7
- **FR-008**: System MUST display Chapter 3 Explorer at sidebar_position 8
- **FR-009**: System MUST display Chapter 3 Builder at sidebar_position 9
- **FR-010**: System MUST display Chapter 3 Engineer at sidebar_position 10
- **FR-011**: Navigation MUST show no interleaving of chapter variants

### Key Entities

- **Chapter Variant**: A chapter document with specific persona path (Explorer/Builder/Engineer)
- **Sidebar Position**: Numeric frontmatter property controlling navigation order
- **Module Index**: The overview page for a module (always first in navigation)

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 9 chapter variant files have unique, non-overlapping sidebar_position values
- **SC-002**: Navigation displays chapters in correct sequential order when site is built
- **SC-003**: Docusaurus build completes without sidebar-related warnings
- **SC-004**: Visual inspection confirms Chapter 1 → Chapter 2 → Chapter 3 ordering

## Assumptions

1. The sidebar position numbering convention will be: position = (chapter_number - 1) * 3 + variant_offset + 1
   - Explorer variant offset: 1
   - Builder variant offset: 2
   - Engineer variant offset: 3
2. Module index remains at position 1
3. No other files in the module directory need sidebar position adjustments
4. Future chapters will follow the same convention

## Scope

### In Scope
- Correcting sidebar_position values in Chapter 2 variant files
- Verifying all chapter files have correct, non-overlapping positions

### Out of Scope
- Modifying Docusaurus configuration files
- Changing the navigation structure or hierarchy
- Adding new navigation features
