## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection UI to the existing SbomListPage so users can select two SBOMs via checkboxes and navigate to the comparison page. This provides the primary entry point for the comparison workflow described in UC-1 of the feature requirements.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row checkboxes and a "Compare selected" action button to the existing SBOM list table

## Implementation Notes
Modify the existing `SbomListPage` in `src/pages/SbomListPage/SbomListPage.tsx` to add:

1. **Row checkboxes**: Add a checkbox column to the existing SBOM list table. Use PatternFly `Table` checkbox selection pattern. Limit selection to exactly two SBOMs — disable further checkboxes when two are selected.
2. **"Compare selected" button**: Add a PatternFly `Button` to the page toolbar (near existing filter controls). Disabled until exactly two SBOMs are selected. On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.

Follow the existing table patterns in `SbomListPage.tsx` for adding columns and toolbar actions.

Use the `FilterToolbar` component from `src/components/FilterToolbar.tsx` as reference for toolbar action placement, though the Compare button may be added directly to the page's toolbar section.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component being modified, demonstrating the current table and toolbar patterns
- `src/components/FilterToolbar.tsx` — reusable toolbar pattern showing how actions are placed in the page toolbar

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select exactly two SBOMs via checkboxes
- [ ] Further checkboxes are disabled when two SBOMs are already selected
- [ ] "Compare selected" button appears in the toolbar area
- [ ] "Compare selected" button is disabled until exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Unit test: verify checkbox column renders in the SBOM list table
- [ ] Unit test: verify "Compare selected" button is disabled with fewer than two selections
- [ ] Unit test: verify "Compare selected" button is enabled with exactly two selections
- [ ] Unit test: verify navigation to the comparison page with correct query parameters on button click
- [ ] Unit test: verify that selecting a third checkbox is prevented when two are already selected

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 6 — Add SBOM comparison page UI
