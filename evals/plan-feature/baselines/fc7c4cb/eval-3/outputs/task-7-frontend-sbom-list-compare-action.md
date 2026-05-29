## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection and a "Compare selected" action button to the existing SBOM list page. Users select exactly two SBOMs via checkboxes, then click "Compare selected" to navigate to the comparison page with the selected SBOM IDs as URL query parameters. This implements the UC-1 entry point for the comparison workflow.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the SBOM table and a "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Figma design context:** The SBOM list page should have row-level checkbox selection using PatternFly `Table` composable table's built-in select functionality. The "Compare selected" button should appear in the toolbar area, styled as a secondary PatternFly `Button`, disabled until exactly two SBOMs are selected.
- Follow the existing table pattern in `src/pages/SbomListPage/SbomListPage.tsx` — add a selection column to the existing table configuration.
- Use PatternFly's composable `Table` select pattern — add `onSelect` handler and `isSelected` state tracking using React `useState` for selected row IDs.
- The "Compare selected" button should use React Router's `useNavigate` hook to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.
- Reference the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` for toolbar action button placement patterns.
- Disable the "Compare selected" button when fewer or more than two SBOMs are selected. Show a tooltip or helper text indicating "Select exactly 2 SBOMs to compare".

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page being modified; understand its current table and toolbar structure before adding selection
- `src/components/FilterToolbar.tsx` — existing toolbar component pattern for reference on action button placement

## Acceptance Criteria
- [ ] SBOM list table has a checkbox selection column
- [ ] Users can select and deselect SBOMs via checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs

## Test Requirements
- [ ] Unit test: verify checkbox selection column renders in the SBOM table
- [ ] Unit test: verify "Compare selected" button is disabled when 0 or 1 SBOMs are selected
- [ ] Unit test: verify "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Unit test: verify clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page (route must exist for navigation target)

[sdlc-workflow] Description digest: sha256:b6b2651519f4051096bc2fee8f173b5d9e20e6eeb6af1d122dc25a58774ea324
