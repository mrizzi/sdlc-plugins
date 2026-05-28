# Task 7 — Add "Compare selected" functionality to SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection and a "Compare selected" button to the SBOM list page, allowing users to select exactly two SBOMs and navigate to the comparison page with the selected IDs. This implements the entry point for the comparison workflow described in UC-1 of the feature.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes to the SBOM table, add a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected

## Implementation Notes
- Follow the existing table pattern in `src/pages/SbomListPage/SbomListPage.tsx`. Add PatternFly table row selection using the composable `Table` select feature — add a checkbox column and track selected row IDs in component state.
- The "Compare selected" button should be a PatternFly secondary `Button` in the toolbar area. It should be disabled when the number of selected SBOMs is not exactly 2.
- On click, navigate using React Router's `useNavigate` to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.
- Keep the button visually grouped with other toolbar actions if any exist (e.g., near filters).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the file being modified; its existing table and toolbar structure must be preserved and extended
- `src/components/FilterToolbar.tsx` — existing toolbar component that may inform toolbar button placement

## Acceptance Criteria
- [ ] SBOM list table rows have selection checkboxes
- [ ] "Compare selected" button is visible in the toolbar area
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is cleared after navigation

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, and 3 selected SBOMs
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selected SBOMs
- [ ] Unit test: clicking the button navigates to the correct comparison URL with selected SBOM IDs
- [ ] Update existing `SbomListPage.test.tsx` tests if any are affected by the new checkbox column

## Dependencies
- Depends on: Task 6 — Add SBOM comparison page with diff sections
