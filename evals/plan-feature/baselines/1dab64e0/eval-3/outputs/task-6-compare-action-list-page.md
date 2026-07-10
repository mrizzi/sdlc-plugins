## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection and a "Compare selected" action button to the SBOM list page, enabling users to select two SBOMs and navigate to the comparison page. This is the entry point for the comparison workflow described in UC-1 of the feature requirements.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row checkboxes for SBOM selection (max 2), a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}`, and selection state management

## Implementation Notes
Modify the existing SBOM list table in `src/pages/SbomListPage/SbomListPage.tsx` to support row selection:

1. Add PatternFly `Table` row selection using the `select` property on table rows. Limit selection to exactly 2 rows — disable further checkboxes when 2 are selected.
2. Add a "Compare selected" `Button` to the page toolbar (alongside existing filter controls). The button should:
   - Be disabled when fewer than 2 SBOMs are selected
   - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
3. Manage selection state using React `useState` with an array of selected SBOM IDs.

Follow the toolbar layout pattern used by `src/components/FilterToolbar.tsx` for adding the action button alongside existing controls.

Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md: use React Router v6 for navigation.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` routing scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing page being modified; contains the table and toolbar structure to extend
- `src/components/FilterToolbar.tsx` — Reference for PatternFly toolbar layout with action buttons

## Acceptance Criteria
- [ ] SBOM list page rows have checkboxes for selection
- [ ] Selection is limited to a maximum of 2 SBOMs
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Unit test: checkboxes render on each SBOM list row
- [ ] Unit test: selecting more than 2 SBOMs is prevented
- [ ] Unit test: "Compare selected" button is disabled with fewer than 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with selected IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections (comparison page must exist for navigation target)
