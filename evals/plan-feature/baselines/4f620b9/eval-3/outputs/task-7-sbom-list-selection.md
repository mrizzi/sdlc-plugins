## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection checkboxes and a "Compare selected" action button to the existing SbomListPage, enabling users to select two SBOMs from the list and navigate to the comparison view. This implements the entry point for UC-1 (Compare two SBOM versions) from the feature requirements.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes and "Compare selected" toolbar action

## Implementation Notes
- Follow the PatternFly Table selection pattern — add `select` configuration to the Table component to enable checkbox-based row selection.
- Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`).
- Add a "Compare selected" PatternFly `Button` to the page toolbar (near the filter toolbar area), disabled until exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router `useNavigate`.
- Limit selection to a maximum of two rows — when a third row is selected, deselect the oldest selection (FIFO behavior) or disable further selections with a tooltip explaining "Select exactly two SBOMs to compare."
- Use the existing `FilterToolbar` component pattern from `src/components/FilterToolbar.tsx` for toolbar layout consistency.

**Figma component mapping:**
| Figma Element | PatternFly Component |
|---|---|
| Row checkboxes | `Table` select prop |
| Compare selected button | `Button` (variant="secondary") |

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page being modified, follow its current patterns
- `src/components/FilterToolbar.tsx` — toolbar layout pattern for placing the Compare button

## Acceptance Criteria
- [ ] SbomListPage table rows have selection checkboxes
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled until exactly two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection is limited to two SBOMs maximum

## Test Requirements
- [ ] Unit test: checkboxes render on each table row
- [ ] Unit test: "Compare selected" button is disabled with fewer than two selections
- [ ] Unit test: "Compare selected" button navigates to the comparison page with correct query params
- [ ] Unit test: selecting a third SBOM enforces the two-selection limit

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections

[sdlc-workflow] Description digest: sha256-md:0ca4c6dd938822c6dd97068295f056bbf4dcc3c1e2c6bb459fc65757d998e929
