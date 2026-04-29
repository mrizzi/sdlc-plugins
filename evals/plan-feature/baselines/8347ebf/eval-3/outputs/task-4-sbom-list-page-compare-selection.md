# Task 4 — SBOM list page multi-select and Compare navigation

## Repository
trustify-ui

## Description
Add the ability for users to select two SBOMs from the SBOM list page and navigate to the comparison view. This implements UC-1 from the feature specification: users select two SBOMs using checkboxes on the list page and click "Compare selected" to be routed to `/sbom/compare?left={id1}&right={id2}`. The button is disabled until exactly two SBOMs are selected and shows a count indicator.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to the SBOM table, selection state management, and a "Compare selected" button in the toolbar

## Implementation Notes

### Checkbox column
Add a checkbox column as the first column in the SBOM list table. Use PatternFly's composable `Table` checkbox pattern. Each row's checkbox toggles that SBOM's selection state. Selection state is managed via local React state (e.g., `useState<Set<string>>()` tracking selected SBOM IDs).

### Compare selected button
Add a "Compare selected" button to the existing toolbar area (near filters). The button should:
- Be disabled when fewer or more than 2 SBOMs are selected
- Show the selection count (e.g., "Compare selected (2)")
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router `useNavigate`
- The order of `left` and `right` follows the order of selection (first selected = left, second = right)

### Reference patterns
Follow the existing table and toolbar patterns in `SbomListPage.tsx`. The page already uses PatternFly table components and `FilterToolbar` (see `src/components/FilterToolbar.tsx` for toolbar layout reference).

### Relevant constraints
- Per constraints doc section 2 (Commit Rules): commits must reference TC-9003 in the footer, follow Conventional Commits format, and include the `Assisted-by: Claude Code` trailer.
- Per constraints doc section 5 (Code Change Rules): changes must be scoped to listed files; inspect `SbomListPage.tsx` before modifying.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component being modified; inspect current table structure and toolbar layout before adding selection
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for toolbar button placement patterns

## Acceptance Criteria
- [ ] Each row in the SBOM list table has a checkbox column
- [ ] Selecting checkboxes tracks the selected SBOM IDs in component state
- [ ] "Compare selected" button is visible in the toolbar
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Button shows the current selection count
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct IDs
- [ ] Selection state is cleared when navigating away and returning to the list page

## Test Requirements
- [ ] Unit test: checkbox column renders for each row in the SBOM table
- [ ] Unit test: selecting two checkboxes enables the "Compare selected" button
- [ ] Unit test: selecting fewer than 2 or more than 2 disables the button
- [ ] Unit test: clicking "Compare selected" with two SBOMs selected navigates to the correct URL with left and right query params
- [ ] Tests use React Testing Library and MSW handlers from `tests/mocks/handlers.ts`

## Dependencies
- Depends on: Task 3 — Frontend SBOM comparison page with diff sections (the comparison page must exist at `/sbom/compare` for the navigation target to work)
