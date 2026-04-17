# Task 5 — Add "Compare selected" action to SBOM list page

## Repository
trustify-ui

## Description
Add the ability to select two SBOMs from the SBOM list page and navigate to the comparison view. Users select two SBOMs via checkboxes in the list table, then click a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`. This completes the end-to-end user workflow described in UC-1 of the feature.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection to the SBOM table and a "Compare selected" toolbar action

## Implementation Notes
- Add PatternFly table row selection (checkboxes) to the existing SBOM list table. PatternFly composable `Table` supports `select` props for row selection.
- Track selected SBOM IDs in component state. Limit selection to exactly two — after two are selected, disable further checkboxes or show a tooltip.
- Add a "Compare selected" `Button` to the table toolbar. It should be disabled until exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`.
- Follow the existing SbomListPage patterns for toolbar actions and table modifications.
- Per constraints (5.1): scope changes to `SbomListPage.tsx` only — do not modify unrelated files.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page component being modified, contains the table and toolbar structure
- `src/components/FilterToolbar.tsx` — existing toolbar pattern for reference on adding toolbar items

## Acceptance Criteria
- [ ] SBOM list table has checkbox selection per row
- [ ] "Compare selected" button appears in the table toolbar
- [ ] Button is disabled until exactly two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct IDs
- [ ] Existing SBOM list functionality (filtering, pagination, sorting) is not broken

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled when fewer than 2 SBOMs selected
- [ ] Unit test: "Compare selected" button is disabled when more than 2 SBOMs selected
- [ ] Unit test: clicking "Compare selected" with 2 SBOMs navigates to the correct comparison URL
- [ ] Existing SbomListPage tests still pass (no regression)

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — all list page tests pass
- `npx tsc --noEmit` — TypeScript compilation passes

## Dependencies
- Depends on: Task 4 — Add SBOM comparison page with diff sections (the comparison page must exist for navigation to work)
