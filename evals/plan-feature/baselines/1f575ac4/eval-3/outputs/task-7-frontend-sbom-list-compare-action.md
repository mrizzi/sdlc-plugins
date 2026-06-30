## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the ability to select two SBOMs on the SBOM list page and navigate to the comparison view. This includes adding row selection checkboxes to the SBOM table and a "Compare selected" action button that becomes enabled when exactly two SBOMs are selected.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection and "Compare selected" action button

## Implementation Notes
- Add PatternFly `Table` row selection (checkboxes) to the existing SBOM list table in `SbomListPage.tsx`.
- Add a "Compare selected" button to the toolbar area. The button should:
  - Be disabled when fewer or more than 2 SBOMs are selected
  - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
- Follow the existing toolbar and table patterns already in `SbomListPage.tsx`.
- Use PatternFly's `isSelectableRow` and selection state management patterns.
- The selection state should be local component state (not persisted).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table with filters; extend with selection
- `src/components/FilterToolbar.tsx` — toolbar pattern reference for button placement

## Acceptance Criteria
- [ ] SBOM list page shows checkboxes for row selection
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when not exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to the comparison page with correct SBOM IDs in URL params
- [ ] Selection state resets when navigating away and back

## Test Requirements
- [ ] Unit test: verify "Compare selected" button is disabled with 0 or 1 selection
- [ ] Unit test: verify "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: verify navigation to comparison page with correct query params
- [ ] Update existing `SbomListPage.test.tsx` to cover the new selection and compare functionality

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 6 — Frontend comparison page (route must exist for navigation)
