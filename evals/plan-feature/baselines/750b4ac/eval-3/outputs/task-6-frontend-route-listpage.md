# Task 6 — Add comparison route and SbomListPage compare action

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router and add checkbox selection with a "Compare selected" button to the SbomListPage. When two SBOMs are selected and the user clicks "Compare selected", the app navigates to `/sbom/compare?left={id1}&right={id2}`. This completes the user workflow from SBOM list to comparison view.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to SBOM table and "Compare selected" toolbar action

## Implementation Notes
- Follow the routing pattern in `src/routes.tsx`: lazy-load the SbomComparePage component using React Router v6 lazy loading, consistent with other page routes.
- The route for `/sbom/compare` must be registered before `/sbom/:id` to prevent the router from matching "compare" as an SBOM ID parameter.
- For SbomListPage changes:
  - Add a checkbox column to the existing SBOM table (PatternFly `Table` with `select` variant or manual checkbox column).
  - Track selected SBOM IDs in component state. Limit selection to exactly two SBOMs.
  - Add a "Compare selected" button in the toolbar area (PatternFly `Button`, secondary variant). Disabled when fewer or more than 2 SBOMs are selected.
  - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`.
- Reference `src/pages/SbomListPage/SbomListPage.tsx` for the existing table structure and toolbar layout.
- Use the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` as reference for toolbar actions placement.
- Add MSW handlers for the comparison endpoint in `tests/mocks/handlers.ts` for test support.
- Add mock comparison fixture data in `tests/mocks/fixtures/` for testing.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions as pattern
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and toolbar to extend
- `src/components/FilterToolbar.tsx` — toolbar layout pattern for action button placement
- `tests/mocks/handlers.ts` — MSW request handler patterns

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered and renders SbomComparePage
- [ ] SbomListPage table has a checkbox column for selecting SBOMs
- [ ] "Compare selected" button appears in the SbomListPage toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Route ordering prevents `/sbom/compare` from being matched as `/sbom/:id`

## Test Requirements
- [ ] Unit test: SbomListPage renders checkbox column in the table
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with query params
- [ ] E2E test: full workflow — select two SBOMs, click Compare, verify comparison page loads with results

## Verification Commands
- `npx vitest run` — all unit tests pass
- `npx playwright test sbom-compare` — E2E comparison workflow test passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SbomComparePage with diff sections

[sdlc-workflow] Description digest: sha256-md:308fd8ef536aeb713395e78361bee094b2529f636fc3b0ef7f95627a05d05c71
