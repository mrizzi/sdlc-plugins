# Task 6 -- Frontend SBOM List Page Selection and Compare Navigation

## Repository
trustify-ui

## Description
Add checkbox selection to the existing SbomListPage so users can select two SBOMs and navigate to the comparison page. This is the primary entry point for the comparison workflow as described in UC-1: users select two SBOMs from the list, click "Compare selected", and are routed to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox column to the SBOM table, selection state management, and a "Compare selected" toolbar action button

## Implementation Notes
- Follow the existing table patterns in `src/pages/SbomListPage/SbomListPage.tsx`. Add a checkbox select column using PatternFly's Table `select` variant.
- Maintain a selection state (e.g., `useState<string[]>([])`) tracking selected SBOM IDs.
- Add a "Compare selected" button to the page toolbar (alongside existing filter controls). The button should be:
  - Disabled when fewer than 2 SBOMs are selected
  - Disabled when more than 2 SBOMs are selected (optionally show a tooltip explaining "Select exactly 2 SBOMs to compare")
  - Enabled when exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`.
- Reference the existing `FilterToolbar` component (`src/components/FilterToolbar.tsx`) for toolbar layout patterns.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- the file being modified; study its existing table and toolbar structure
- `src/components/FilterToolbar.tsx` -- toolbar layout pattern for adding the Compare button alongside existing controls

## Acceptance Criteria
- [ ] SbomListPage table has a checkbox column for row selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the selected SBOM IDs
- [ ] Selection state is reset when navigating away and back

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is disabled with 3 or more selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL

## Dependencies
- Depends on: Task 5 -- Frontend SBOM Comparison Page (route must be registered)
