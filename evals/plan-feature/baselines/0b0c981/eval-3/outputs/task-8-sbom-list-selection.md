## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection checkboxes and a "Compare selected" button to the existing SBOM list page, enabling users to select two SBOMs and navigate to the comparison page with the selected IDs pre-populated in the URL.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes (limited to two selections), a "Compare selected" toolbar action button, and navigation logic to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
Enhance the existing SBOM list page following PatternFly table selection patterns:

- Add selectable rows to the existing table in `src/pages/SbomListPage/SbomListPage.tsx` using PatternFly's composable `Table` row selection pattern. Limit selection to a maximum of two rows.
- Add a "Compare selected" PatternFly `Button` to the page toolbar (near the existing filter controls referenced by `src/components/FilterToolbar.tsx`). The button is disabled until exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.
- Maintain selection state with `useState<string[]>([])` tracking selected SBOM IDs.
- When a user tries to select a third SBOM, either deselect the first selection or show a PatternFly `Alert` indicating the maximum of two selections. Use a simple deselect-oldest approach for consistency.

**Figma design reference:**
- The "Compare selected" button is a secondary action in the toolbar area, styled as a PatternFly `Button` with variant `secondary`.
- Checkboxes appear in the first column of the SBOM table, using the standard PatternFly `Table` select pattern.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page to modify; contains the table and toolbar layout
- `src/components/FilterToolbar.tsx` — existing toolbar pattern showing how to add actions alongside filters

## Acceptance Criteria
- [ ] SBOM list page displays selection checkboxes on each row
- [ ] Users can select up to two SBOMs
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled when fewer than two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state resets when navigating away and back

## Test Requirements
- [ ] Unit test: verify checkboxes render on SBOM list rows
- [ ] Unit test: verify "Compare selected" button is disabled with zero or one selection
- [ ] Unit test: verify "Compare selected" button is enabled with exactly two selections
- [ ] Unit test: verify clicking "Compare selected" navigates to the correct comparison URL
- [ ] Unit test: verify selecting a third SBOM deselects the oldest selection

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 7 — Add SBOM comparison page with diff sections UI

[sdlc-workflow] Description digest: sha256:9f961f938631491874d4970f9e0d7adafa31d20849d0b909f30c5079cf316403
