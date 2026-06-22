# Task 6 — Add "Compare selected" action to SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add multi-select capability and a "Compare selected" action button to the existing SBOM list page. Users select exactly two SBOMs using checkboxes, then click "Compare selected" to navigate to the comparison page with the selected SBOM IDs as URL query parameters.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column to the SBOM table, track selected SBOMs in component state, add "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- Follow the existing page patterns in `src/pages/SbomListPage/SbomListPage.tsx`.
- Use PatternFly `Table` row selection (checkbox column) to enable multi-select. Track selected rows in React state.
- Add a "Compare selected" button to the page toolbar (alongside any existing actions). The button should:
  - Be disabled when fewer or more than 2 SBOMs are selected
  - Show a tooltip "Select exactly 2 SBOMs to compare" when disabled
  - Navigate to `/sbom/compare?left={id1}&right={id2}` using React Router `useNavigate` when clicked
- Use the first selected SBOM as `left` and the second as `right` in the URL.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page to extend with selection support
- `src/components/FilterToolbar.tsx` — existing toolbar pattern for reference on adding toolbar actions

## Acceptance Criteria
- [ ] SBOM list page table has a checkbox selection column
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Selection state is cleared after navigation

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled when 0, 1, or 3+ SBOMs are selected
- [ ] Unit test: "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections
