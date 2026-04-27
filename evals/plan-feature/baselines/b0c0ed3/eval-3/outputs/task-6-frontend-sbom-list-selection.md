## Repository
trustify-ui

## Description
Add checkbox selection and a "Compare selected" action button to the existing SBOM list page, enabling users to select exactly two SBOMs and navigate to the comparison page. This is the primary entry point for the comparison workflow described in UC-1.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes (PatternFly `Table` select variant) and a "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
**Selection behavior:** Use PatternFly's composable `Table` row selection capabilities. Add a checkbox column to the existing SBOM table. Track selected row IDs in component state using `useState<string[]>`.

**Compare button:** Add a PatternFly `Button` with `variant="secondary"` to the existing toolbar area (near the filters). The button text should be "Compare selected". It should be:
- Hidden or disabled when fewer than 2 SBOMs are selected
- Disabled when more than 2 SBOMs are selected (display a tooltip: "Select exactly two SBOMs to compare")
- Enabled when exactly 2 SBOMs are selected

**Navigation:** On click, use React Router's `useNavigate` hook to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}`.

Follow the existing toolbar pattern in `SbomListPage.tsx` and reference `src/components/FilterToolbar.tsx` for toolbar layout conventions.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — The existing page being modified; review current table and toolbar structure before making changes
- `src/components/FilterToolbar.tsx` — Existing toolbar component pattern; reference for adding the Compare button alongside existing filter actions

## Acceptance Criteria
- [ ] SBOM list table rows have selectable checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Selection state is visually indicated on selected rows

## Test Requirements
- [ ] Unit test: checkboxes render in the SBOM list table
- [ ] Unit test: "Compare selected" button is disabled with 0 selections
- [ ] Unit test: "Compare selected" button is disabled with 1 selection
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: "Compare selected" button is disabled with 3 selections
- [ ] Unit test: clicking "Compare selected" with 2 selections navigates to the correct URL

## Dependencies
- Depends on: Task 5 — Frontend comparison page (the target route must exist for navigation to work)
