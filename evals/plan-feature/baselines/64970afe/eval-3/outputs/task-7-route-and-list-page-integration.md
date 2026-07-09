## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router and add a comparison trigger to the SBOM list page. Users will be able to select two SBOMs using checkboxes on the list page and click a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as URL parameters.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` path mapping to lazy-loaded SbomComparePage component
- `src/pages/SbomListPage/SbomListPage.tsx` — Add PatternFly Table row selection (checkboxes), track selected SBOM IDs in state, add "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- Follow the existing route pattern in `src/routes.tsx` for lazy-loaded page components. Existing routes use React Router v6 with `React.lazy()` imports.
  Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript route definition scope.
- The `/sbom/compare` route must be registered before any `/sbom/:id` route to avoid the path param catching "compare" as an ID.
- In `SbomListPage.tsx`, add PatternFly `Table` selection support:
  - Add checkbox column using PatternFly's composable table `select` transform
  - Track selected rows in component state as an array of SBOM IDs
  - Add a PatternFly `Button` labeled "Compare selected" in the toolbar area (near existing filter controls)
  - Button is disabled when fewer than 2 SBOMs are selected
  - On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router `useNavigate`
  - If more than 2 SBOMs are selected, use only the first two (or show a warning)
- Reference the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` for toolbar layout patterns.

- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TSX component scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions; extend with comparison route following same pattern
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page with table and filters; extend with selection and compare button
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for toolbar button placement

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered and loads the SbomComparePage component
- [ ] SBOM list page displays checkboxes for row selection
- [ ] "Compare selected" button appears in the SBOM list page toolbar
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with selected SBOM IDs
- [ ] Navigation to `/sbom/compare` via direct URL works (route is accessible)

## Test Requirements
- [ ] Test: `/sbom/compare` route renders the SbomComparePage component
- [ ] Test: SBOM list page renders checkboxes for each row
- [ ] Test: "Compare selected" button is disabled when no SBOMs are selected
- [ ] Test: "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Test: clicking "Compare selected" navigates to the correct comparison URL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Implement SBOM comparison page with diff sections
