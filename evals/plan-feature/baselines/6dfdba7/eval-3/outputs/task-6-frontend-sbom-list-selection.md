## Repository
trustify-ui

## Description
Add multi-select capability to the SBOM list page so users can select two SBOMs and navigate to the comparison page. This implements UC-1 from the feature requirements: the user selects two SBOMs using checkboxes on the list page and clicks "Compare selected" to open the comparison view. This is the primary entry point for the comparison workflow.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- Add row checkboxes for multi-selection, a "Compare selected" button in the toolbar, and navigation logic to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Checkbox selection**: Add a PatternFly `Table` select variant to the existing SBOM list table. Use PatternFly's composable table checkbox pattern -- add a checkbox column as the first column. Track selected row IDs in component state using `useState<string[]>([])`.
- **"Compare selected" button**: Add a PatternFly `Button` (variant: `primary`) to the existing toolbar area (alongside any existing filter controls from `src/components/FilterToolbar.tsx`). The button text should be "Compare selected". It should be:
  - Hidden or disabled when fewer than 2 SBOMs are selected
  - Disabled when more than 2 SBOMs are selected (with a tooltip: "Select exactly two SBOMs to compare")
  - Enabled when exactly 2 SBOMs are selected
- **Navigation**: When the user clicks "Compare selected", use React Router's `useNavigate` to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`. Follow the existing navigation patterns in the codebase.
- **Figma alignment**: The "Compare selected" button uses a PatternFly primary `Button` component. When disabled, use a PatternFly `Tooltip` wrapping the button to explain why it is disabled. This follows PatternFly's accessibility guidelines for disabled interactive elements.
- **Preserve existing functionality**: The SBOM list page already has table rendering, filtering, and pagination. The checkbox selection and compare button are additive -- do not change the existing table columns, filters, or pagination behavior.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` -- The existing toolbar component; add the "Compare selected" button alongside existing toolbar items
- `src/pages/SbomListPage/SbomListPage.tsx` -- The existing page component being modified; understand its current table and toolbar structure before adding selection
- `src/routes.tsx` -- Verify the `/sbom/compare` route exists (added in Task 5) for navigation target

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Existing table functionality (columns, filters, pagination, sorting) is not broken
- [ ] Tooltip explains why the button is disabled when selection count is not exactly 2

## Test Requirements
- [ ] Unit test: checkbox selection toggles row selection state
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selected SBOMs
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selected SBOMs
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs as query params
- [ ] Existing SbomListPage tests in `src/pages/SbomListPage/SbomListPage.test.tsx` continue to pass

## Verification Commands
- `npx vitest run SbomListPage` -- should pass all tests including new selection tests

## Dependencies
- Depends on: Task 5 -- Build SBOM comparison page with diff sections (the comparison page must exist as the navigation target)
