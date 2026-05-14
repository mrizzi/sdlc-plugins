# Task 6: Add comparison selection to SBOM list page

## Repository
trustify-ui

## Target Branch
main

## Description
Modify the existing SBOM list page to support selecting two SBOMs for comparison. Add checkbox selection to the SBOM table and a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as query parameters. This implements the primary entry point for the comparison workflow described in UC-1 of the feature spec.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and a "Compare selected" action button in the toolbar

## Implementation Notes
- **Checkbox selection in the SBOM table**:
  - Add a PatternFly `Table` checkbox column as the first column. PatternFly composable tables support row selection via `select` property on each row.
  - Manage selection state with `useState<string[]>([])` tracking selected SBOM IDs.
  - Limit selection to exactly 2 SBOMs. When 2 are selected, disable further checkboxes on unselected rows (or show a visual hint that the maximum is reached).

- **Compare selected button**:
  - Add a primary action button labeled "Compare selected" to the existing toolbar area (where `FilterToolbar` from `src/components/FilterToolbar.tsx` is rendered).
  - Button is disabled when fewer than 2 SBOMs are selected.
  - On click, navigate using React Router's `useNavigate` to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.

- **Figma design alignment**:
  - The "Compare selected" button should use PatternFly `Button` with `variant="primary"`.
  - The button should appear alongside the existing filter toolbar, following the PatternFly toolbar layout pattern.
  - When exactly 2 SBOMs are selected, show a PatternFly `Badge` on the button showing "2 selected" or similar indicator.

- **Existing code references**:
  - The SBOM list table in `src/pages/SbomListPage/SbomListPage.tsx` already renders SBOMs in a table — add the checkbox column alongside existing columns.
  - The `useSboms` hook in `src/hooks/useSboms.ts` provides the SBOM data.
  - Follow the existing router navigation patterns in the codebase (`useNavigate` from React Router v6).

## Acceptance Criteria
- [ ] SBOM list page table has a checkbox column for row selection
- [ ] Users can select exactly 2 SBOMs using checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is cleared on page navigation away and back
- [ ] Existing SBOM list functionality (filtering, pagination, sorting) is not broken

## Test Requirements
- [ ] Unit test: checkbox column renders for each row in the SBOM table
- [ ] Unit test: "Compare selected" button is disabled when 0 or 1 SBOMs are selected
- [ ] Unit test: "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs

## Dependencies
- Depends on: Task 5 — Build the SBOM comparison page UI (the navigation target must exist)
