## Repository
trustify-ui

## Description
Add SBOM selection checkboxes and a "Compare selected" action button to the existing SBOM list page. This enables the entry point for the comparison workflow: users select two SBOMs from the list and click "Compare selected" to navigate to the comparison page with the selected SBOM IDs in the URL.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes to the SBOM table, track selected SBOM IDs in state, and add a "Compare selected" button to the toolbar that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- In `src/pages/SbomListPage/SbomListPage.tsx`, add PatternFly table row selection using the composable `Table` checkbox pattern. Track selected rows in local component state as an array of SBOM IDs.
- Add a "Compare selected" button to the existing toolbar area (reference `src/components/FilterToolbar.tsx` for toolbar patterns). The button should:
  - Be disabled when fewer or more than 2 SBOMs are selected
  - Use PatternFly `Button` with `variant="secondary"`
  - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
- Show a PatternFly `Tooltip` on the disabled button explaining "Select exactly 2 SBOMs to compare".
- The selection state should be cleared when navigating away or when filters change.
- Follow existing page patterns: `SbomListPage.tsx` already has a table and toolbar, so this adds to the existing structure rather than replacing it.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Extend the existing table with selection capability
- `src/components/FilterToolbar.tsx` — Reference for toolbar layout and PatternFly toolbar usage

## Acceptance Criteria
- [ ] SBOM list table rows have selection checkboxes
- [ ] Users can select exactly two SBOMs
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when not exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Tooltip appears on the disabled button explaining the selection requirement

## Test Requirements
- [ ] Unit test: checkboxes render on each table row
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking the button navigates to the correct comparison URL with selected IDs

## Dependencies
- Depends on: Task 5 — SBOM comparison page (the target page must exist for navigation)
