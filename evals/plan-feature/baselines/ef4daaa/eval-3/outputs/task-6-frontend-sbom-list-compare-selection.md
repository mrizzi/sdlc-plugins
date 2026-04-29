# Task 6 — Frontend SBOM list page compare selection

## Repository
trustify-ui

## Description
Modify the SBOM list page to support selecting two SBOMs and navigating to the comparison page. Add row checkboxes for multi-selection (limited to two) and a "Compare selected" action button that navigates to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection and "Compare selected" button to the existing SBOM list table

## Implementation Notes
- **Selection mechanism**: add PatternFly checkbox column to the existing SBOM table. Limit selection to a maximum of two SBOMs. When a third is selected, either deselect the oldest selection or show a tooltip explaining the two-SBOM limit.
- **"Compare selected" button**: add a primary action button in the toolbar area (near filters). The button should:
  - Be disabled when fewer than two SBOMs are selected
  - Show text "Compare selected" with the count when exactly two are selected
  - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
- **Follow existing patterns**: the `SbomListPage.tsx` already uses PatternFly table with `FilterToolbar` (see `src/components/FilterToolbar.tsx`). Add the Compare button alongside existing toolbar actions.
- **Selection state**: use React `useState` to track selected SBOM IDs as an array of up to two IDs.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page being modified; follow its existing toolbar and table patterns
- `src/components/FilterToolbar.tsx` — existing toolbar component where the Compare button may be placed

## Acceptance Criteria
- [ ] SBOM list table has selectable checkboxes on each row
- [ ] Maximum of two SBOMs can be selected at once
- [ ] "Compare selected" button appears in the toolbar area
- [ ] "Compare selected" button is disabled when fewer than two SBOMs are selected
- [ ] "Compare selected" button is enabled when exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Unit test: checkboxes appear on each SBOM row
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: "Compare selected" button is disabled with zero or one selection
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Dependencies
- Depends on: Task 5 — Frontend SBOM comparison page (the target page must exist for navigation)
