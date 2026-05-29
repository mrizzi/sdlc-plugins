# Task 7 — Add checkbox selection and Compare action to SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enhance the existing SBOM list page with checkbox selection and a "Compare selected" button that navigates to the comparison page with the two selected SBOM IDs as URL query parameters. This enables the primary user workflow of selecting two SBOMs from the list and comparing them.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- Add a checkbox column to the existing SBOM table using PatternFly's composable `Table` select pattern. Track selected row IDs in component state.
- Add a "Compare selected" button to the page toolbar (next to existing filter controls). The button should be:
  - Disabled when fewer than 2 SBOMs are selected
  - Disabled when more than 2 SBOMs are selected (comparison is pairwise only)
  - Enabled when exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`.
- Follow the existing toolbar pattern in `src/components/FilterToolbar.tsx` for toolbar layout.
- Reference the existing `SbomListPage.tsx` for the current table structure and column definitions.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page being modified, provides the current table and toolbar layout
- `src/components/FilterToolbar.tsx` — existing toolbar component pattern for consistent toolbar layout

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct IDs
- [ ] Selection state resets when navigating away and back

## Test Requirements
- [ ] Unit test: checkbox selection toggles correctly
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking the button navigates to the comparison page with correct query params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections
