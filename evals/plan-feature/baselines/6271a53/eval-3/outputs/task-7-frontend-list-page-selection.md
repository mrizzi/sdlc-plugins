# Task 7 — Add SBOM selection and "Compare selected" to list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection to the SBOM list page and a "Compare selected" action button. When a user selects exactly two SBOMs and clicks "Compare selected", they are navigated to `/sbom/compare?left={id1}&right={id2}`. This implements the primary user workflow (UC-1) for initiating a comparison from the SBOM list.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and "Compare selected" toolbar action

## Implementation Notes
- Add a checkbox column to the existing SBOM list table using PatternFly's composable Table select pattern
- Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`)
- Add a "Compare selected" button to the page toolbar, styled as a PatternFly `Button` variant="secondary"
- The button should be disabled unless exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
- Follow the existing toolbar and action button patterns in `SbomListPage.tsx`
- Keep the existing table columns and functionality intact — this is an additive change

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the file being modified; follow its existing toolbar and table patterns
- `src/components/FilterToolbar.tsx` — reference for toolbar action button placement

## Acceptance Criteria
- [ ] Checkboxes appear in the SBOM list table for each row
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Existing SBOM list functionality is not broken

## Test Requirements
- [ ] Unit test: checkboxes render in each table row
- [ ] Unit test: "Compare selected" button is disabled by default
- [ ] Unit test: selecting exactly 2 SBOMs enables the button
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs
- [ ] Unit test: selecting 3 SBOMs disables the button

## Dependencies
- Depends on: Task 6 — Create SBOM comparison page with diff sections
