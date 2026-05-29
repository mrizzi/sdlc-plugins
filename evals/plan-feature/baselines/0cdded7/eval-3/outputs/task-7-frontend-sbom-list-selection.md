# Task 7 — Add SBOM selection checkboxes and Compare action to SbomListPage

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Extend the existing SBOM list page to support multi-selection of SBOMs via checkboxes and add a "Compare selected" toolbar action that navigates to the comparison page with the two selected SBOM IDs encoded in URL query params. This provides the primary entry point for the comparison workflow (UC-1 from the feature description).

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to the SBOM table, track selected items in component state, add "Compare selected" button to the toolbar that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- Use PatternFly's composable `Table` checkbox selection pattern — add a select column with `onSelect` handlers. Track selection state as an array of selected SBOM IDs in component state.
- The "Compare selected" button should be placed in the existing toolbar area (near any existing action buttons). It should be disabled when fewer or more than 2 SBOMs are selected, with a tooltip explaining "Select exactly 2 SBOMs to compare".
- Use React Router's `useNavigate` hook to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` when the button is clicked.
- Follow the existing `SbomListPage.tsx` patterns for toolbar layout and button placement.
- The selection state should reset when the page filters or pagination change.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the file being modified; understand its existing table and toolbar structure
- `src/components/FilterToolbar.tsx` — toolbar pattern for action button placement reference

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Button tooltip indicates "Select exactly 2 SBOMs to compare" when disabled
- [ ] Clicking the button with 2 selected SBOMs navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state resets when filters or pagination change

## Test Requirements
- [ ] Unit test: verify checkbox column renders in the SBOM table
- [ ] Unit test: verify "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: verify navigation to comparison page with correct query params when 2 SBOMs are selected and button is clicked
- [ ] Update existing `SbomListPage.test.tsx` to ensure existing tests still pass with the new checkbox column

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections

[sdlc-workflow] Description digest: sha256:36f6a65b0da4f8ec85b6d1ff5d90e7115e4154096c06a34ff8f6f4315daddc71
