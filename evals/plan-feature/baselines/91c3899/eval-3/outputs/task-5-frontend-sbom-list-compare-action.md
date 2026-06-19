# Task 5 — Add compare action to SBOM list page

## Repository
trustify-ui

## Target Branch
main

## Description
Add checkbox selection to the SBOM list table and a "Compare selected" toolbar action that navigates to the comparison page with the two selected SBOM IDs as URL query parameters. This implements the user flow from UC-1 where users select two SBOMs from the list page and initiate a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes to the SBOM table, add "Compare selected" button to the toolbar, implement navigation to `/sbom/compare?left={id1}&right={id2}` when two SBOMs are selected

## Implementation Notes
- Use PatternFly `Table` row selection (checkbox variant) to enable multi-select on the existing SBOM list table. See `src/pages/SbomDetailPage/components/PackageTable.tsx` for PatternFly Table usage patterns in the codebase.
- Add a "Compare selected" `Button` to the page toolbar. The button should be disabled unless exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate` hook.
- Maintain selected SBOM IDs in local component state (useState). Clear selection when the table data changes (e.g., on filter or pagination changes).
- Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM list page; extend with selection capabilities
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing PatternFly Table implementation; reference for row selection patterns

## Acceptance Criteria
- [ ] Each row in the SBOM list table has a selection checkbox
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking the button navigates to /sbom/compare with correct left and right query parameters
- [ ] Selection state is cleared on filter or pagination changes

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled when no SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when only one SBOM is selected
- [ ] Unit test: "Compare selected" button is enabled when exactly two SBOMs are selected
- [ ] Unit test: clicking "Compare selected" with two selected SBOMs navigates to the correct URL
- [ ] Unit test: selecting a third SBOM disables the "Compare selected" button

## Dependencies
- Depends on: Task 4 — Add SBOM comparison page
