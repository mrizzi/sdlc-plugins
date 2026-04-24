# Task 5 — Frontend SBOM list page comparison selection UX

## Repository
trustify-ui

## Description
Add the ability for users to select two SBOMs from the SBOM list page and navigate to the comparison view. This implements UC-1 from the feature requirements: the user selects two SBOMs using checkboxes on the list page, clicks a "Compare selected" button, and is navigated to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to the SBOM table, selection state management, and "Compare selected" action button

## Implementation Notes
- Follow the existing SbomListPage structure in `src/pages/SbomListPage/SbomListPage.tsx`. Add a checkbox column to the existing SBOM table to allow row selection.
- Use PatternFly's composable `Table` selection features (or `Select` row variant) to add checkboxes. Limit selection to exactly 2 rows — disable additional checkboxes once 2 SBOMs are selected, or use a PatternFly toolbar action that enables only when exactly 2 are selected.
- Add a "Compare selected" button in the page toolbar (near existing filters or actions). The button should:
  - Be disabled when fewer or more than 2 SBOMs are selected
  - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate()` hook
- Selection state should be managed locally within the component (React `useState`) — no need for global state since selections are ephemeral.
- The button label should be "Compare selected" to match the feature description's UC-1 workflow.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page being modified; follow its existing patterns for toolbar actions
- `src/components/FilterToolbar.tsx` — existing toolbar component; check if the "Compare selected" button integrates into this or is a sibling component

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select exactly 2 SBOMs using checkboxes
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Selection state resets after navigation (or on page return)

## Test Requirements
- [ ] Unit test: checkbox column renders in the SBOM list table
- [ ] Unit test: "Compare selected" button is disabled when no SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when only 1 SBOM is selected
- [ ] Unit test: "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Dependencies
- Depends on: Task 4 — Frontend SBOM comparison page with diff sections (the target route must exist)
