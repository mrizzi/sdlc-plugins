## Repository
trustify-ui

## Description
Update the SBOM list page to support selecting two SBOMs for comparison. Add row checkboxes (max 2 selections) and a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to SBOM table, selection state (max 2), and "Compare selected" button in toolbar

## Implementation Notes
- Add a checkbox column to the existing SBOM table using PatternFly `Table` composable with `Select` column type.
- Manage selection state with React `useState` — track selected SBOM IDs as an array, enforce max 2 selections.
- Add "Compare selected" button (PatternFly `Button`, variant secondary) to the page toolbar. Disable when fewer than 2 SBOMs are selected.
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router `useNavigate`.
- Follow the existing `SbomListPage` patterns in `src/pages/SbomListPage/SbomListPage.tsx` for table rendering and toolbar layout.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page to modify, reference for table and toolbar patterns
- `src/components/FilterToolbar.tsx` — reference for toolbar button placement

## Acceptance Criteria
- [ ] SBOM list page has checkbox column for row selection
- [ ] Maximum 2 SBOMs can be selected at a time
- [ ] "Compare selected" button appears in toolbar, disabled when < 2 selected
- [ ] Clicking "Compare selected" navigates to comparison page with correct SBOM IDs in URL

## Test Requirements
- [ ] Component test: checkboxes render and track selection state
- [ ] Component test: third checkbox selection is prevented or replaces oldest selection
- [ ] Component test: "Compare selected" button is disabled with fewer than 2 selections
- [ ] Component test: navigation to comparison page includes correct query params

## Dependencies
- Depends on: Task 5 — SBOM compare page (compare page must exist to navigate to)
