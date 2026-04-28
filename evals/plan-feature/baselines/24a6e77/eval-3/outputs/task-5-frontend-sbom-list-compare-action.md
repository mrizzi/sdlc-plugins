# Task 5 — Frontend: Add SBOM multi-select and "Compare selected" action to SBOM list page

## Repository
trustify-ui

## Description
Add the ability for users to select two SBOMs from the SBOM list page using checkboxes and click a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as URL query parameters. This implements the primary entry point for the comparison workflow described in UC-1.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and "Compare selected" toolbar action

## Implementation Notes

### Selection mechanism

Add PatternFly table row selection (checkboxes) to the existing SBOM list table in `SbomListPage.tsx`:
- Use PatternFly's composable `Table` select functionality (row checkboxes)
- Track selected SBOM IDs in component state using `useState<string[]>([])`
- Limit selection to exactly two SBOMs — disable additional checkboxes once two are selected, or show a validation message if the user tries to select more

### "Compare selected" button

Add a "Compare selected" button in the toolbar area (alongside existing filter controls):
- Use PatternFly `Button` with variant `secondary`
- Disabled when fewer than two SBOMs are selected
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate` hook
- Show count of selected items in the button label or nearby, e.g., "Compare selected (2)"

Follow the existing toolbar layout patterns in `src/pages/SbomListPage/SbomListPage.tsx` and the `FilterToolbar` component in `src/components/FilterToolbar.tsx`.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page to modify; reference for table and toolbar layout
- `src/components/FilterToolbar.tsx` — existing toolbar component for layout reference

## Acceptance Criteria
- [ ] SBOM list table rows have selection checkboxes
- [ ] Users can select exactly two SBOMs
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer than two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is visually clear (selected rows are highlighted)

## Test Requirements
- [ ] Unit test: checkboxes render in each SBOM table row
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: clicking "Compare selected" navigates to the comparison page with correct query params
- [ ] Unit test: selecting fewer than two SBOMs keeps the button disabled

## Dependencies
- Depends on: Task 4 — Frontend: SBOM comparison page UI and routing (comparison page must exist for navigation target)
