# Task 7: Add compare action to SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Modify the existing SBOM list page to add checkbox selection and a "Compare selected" action button. When the user selects exactly two SBOMs via checkboxes, the "Compare selected" button becomes enabled. Clicking it navigates to the comparison page (`/sbom/compare?left={id1}&right={id2}`) with the selected SBOM IDs as query parameters.

## Figma Design Reference
The Figma design specifies the following selection UX on the SBOM list page:

- **Checkbox column**: Add a checkbox column as the first column in the SBOM list table, enabling multi-row selection
- **"Compare selected" button**: Placed in the toolbar area above the table. Disabled when fewer or more than two SBOMs are selected. Uses PatternFly `Button` with `variant="primary"`
- **Selection count indicator**: Show the number of selected SBOMs near the button (e.g., "2 selected")

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the table, selection state management, "Compare selected" button in the toolbar, and navigation logic to the comparison page

## Implementation Notes
- The SBOM list page already uses a PatternFly `Table` component. Add a checkbox column using PatternFly's composable table `Td` with `select` props for row-level checkboxes.
- Manage selection state with React `useState<string[]>` to track selected SBOM IDs.
- The "Compare selected" button should:
  1. Be placed in the toolbar alongside existing filter controls.
  2. Be disabled when `selectedIds.length !== 2`.
  3. On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`.
- Follow the existing pattern in `SbomListPage.tsx` for toolbar layout and button placement.
- Clear selection state when filters change or when the page is navigated away from.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page being modified
- `src/components/FilterToolbar.tsx` — reference for toolbar layout patterns
- `src/routes.tsx` — verify the `/sbom/compare` route exists (added in Task 6)

## Acceptance Criteria
- [ ] Each row in the SBOM list table has a checkbox for selection
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Button is enabled when exactly two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state resets on filter changes

## Test Requirements
- [ ] Unit test: checkbox column renders in the table
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking the button navigates to the correct comparison URL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Create SBOM comparison page (route must be registered)

`[sdlc-workflow] Description digest: sha256-md:a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9`
