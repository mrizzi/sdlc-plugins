# Task 6 — Frontend SBOM list page selection and compare navigation

## Repository
trustify-ui

## Description
Enhance the existing SBOM List Page to support multi-selection of exactly two SBOMs and provide a "Compare selected" action button that navigates to the comparison page with the selected SBOM IDs encoded in the URL. This implements the primary user workflow (UC-1) where users select two SBOMs from the list and initiate a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the SBOM table, selection state management (max 2), and a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- The existing `SbomListPage` in `src/pages/SbomListPage/SbomListPage.tsx` renders a table of SBOMs with filters. Add a checkbox selection column using PatternFly's `Table` composable selection pattern.
- Maintain selection state with React's `useState` — store an array of selected SBOM IDs (max 2).
- When the user selects a third SBOM, either deselect the oldest selection or disable further checkboxes. A simple approach is to disable checkboxes for unselected rows when 2 are already selected.
- Add a "Compare selected" button to the page toolbar (above the table, next to existing filter controls). The button should be disabled when fewer than 2 SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`.
- Follow the existing `SbomListPage` component patterns for toolbar layout and PatternFly component usage.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page to modify, reference its table and toolbar patterns
- `src/components/FilterToolbar.tsx` — existing toolbar component for consistent toolbar layout

## Acceptance Criteria
- [ ] SBOM list table has a checkbox selection column
- [ ] Users can select exactly two SBOMs via checkboxes
- [ ] Selecting more than two SBOMs is prevented (checkboxes disabled or oldest deselected)
- [ ] "Compare selected" button appears in the toolbar
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is visually clear (selected rows highlighted)

## Test Requirements
- [ ] Unit test: checkbox selection column is rendered in the SBOM table
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: selecting fewer than two SBOMs keeps the button disabled
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both IDs
- [ ] Unit test: selecting a third SBOM is prevented when two are already selected

## Dependencies
- Depends on: Task 5 — Frontend SBOM Comparison Page (the target page must exist for navigation)
