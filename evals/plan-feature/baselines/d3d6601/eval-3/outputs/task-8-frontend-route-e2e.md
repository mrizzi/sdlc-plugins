## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router and implement URL query parameter handling so that comparison URLs are shareable. Add mock data fixtures and an E2E test covering the full comparison workflow: selecting two SBOMs, clicking Compare, and verifying the diff sections render.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection for SBOMs and a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison API response fixture for tests
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Implementation Notes
- **Route registration**: Add a route entry in `src/routes.tsx` following the existing pattern (e.g., the SBOM detail page route). Use lazy loading via `React.lazy()` for the `SbomComparePage` component, consistent with the existing routing pattern.
- **URL query parameter handling**: The `SbomComparePage` should read `left` and `right` from URL search params using `useSearchParams()` from React Router. Pre-populate the SBOM selectors from these params. When the user clicks "Compare", update the URL search params to make the URL shareable.
- **SBOM list page integration**: Add PatternFly checkbox selection to the SBOM list table in `src/pages/SbomListPage/SbomListPage.tsx`. Add a "Compare selected" button (enabled when exactly 2 SBOMs are selected) that navigates to `/sbom/compare?left={id1}&right={id2}` using `useNavigate()`.
- **Mock fixture**: Create `tests/mocks/fixtures/sbom-comparison.json` following the same structure as `tests/mocks/fixtures/sboms.json` — provide a sample `SbomComparison` response with at least one item in each diff section.
- **MSW handler**: Add a handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts` that returns the mock fixture.
- **E2E test**: Follow the pattern in `tests/e2e/sbom-list.spec.ts` for the Playwright test structure. The test should:
  1. Navigate to the SBOM list page
  2. Select two SBOMs
  3. Click "Compare selected"
  4. Verify the comparison page loads with diff sections
  5. Verify the URL contains the correct query parameters

## Reuse Candidates
- `src/routes.tsx` — existing route definitions; follow the same lazy loading and path patterns
- `tests/mocks/handlers.ts` — existing MSW handlers; add the comparison endpoint handler following the same pattern
- `tests/mocks/fixtures/sboms.json` — reference fixture format for creating the comparison fixture
- `tests/e2e/sbom-list.spec.ts` — reference E2E test structure and Playwright patterns
- `tests/setup.ts` — test setup with MSW and render helpers

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered in `src/routes.tsx` and loads the comparison page
- [ ] URL query params `left` and `right` pre-populate the SBOM selectors
- [ ] Changing the comparison updates the URL for shareability (UC-2)
- [ ] SBOM list page has checkbox selection and "Compare selected" button
- [ ] "Compare selected" button navigates to comparison page with correct query params
- [ ] E2E test passes covering the full comparison workflow

## Test Requirements
- [ ] E2E test: select two SBOMs on list page, click "Compare selected", verify comparison page renders with diff sections
- [ ] E2E test: navigate directly to `/sbom/compare?left={id1}&right={id2}` — verify comparison loads from URL params
- [ ] Unit test: verify route `/sbom/compare` renders `SbomComparePage` component
- [ ] Unit test: verify "Compare selected" button is disabled when fewer than 2 SBOMs are selected

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 7 — Add SBOM comparison page UI with diff sections

[sdlc-workflow] Description digest: sha256:2783ca99c5f8f73ca3785c8da0492cc02035cad912611ba35eac5558bf6e635a
