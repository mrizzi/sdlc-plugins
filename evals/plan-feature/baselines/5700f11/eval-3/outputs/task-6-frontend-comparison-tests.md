## Repository
trustify-ui

## Description
Add MSW mock handlers, test fixtures, and E2E tests for the SBOM comparison feature. This includes mock data for the comparison API response, MSW handler registration for use in unit tests, and a Playwright E2E test that exercises the full comparison workflow from SBOM selection through diff rendering.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` that returns the mock comparison fixture

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture with representative data across all six diff sections (added packages, removed packages, version changes, new vulnerabilities including a Critical severity entry, resolved vulnerabilities, license changes)
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page using React Testing Library with MSW mocking
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Implementation Notes
- **Mock fixture**: Create `tests/mocks/fixtures/sbom-comparison.json` following the pattern in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`. Include at least 2-3 items in each diff section to provide meaningful test data. Include at least one entry with `"severity": "critical"` in `new_vulnerabilities` to test the highlighted row styling.
- **MSW handler**: In `tests/mocks/handlers.ts`, add a handler for `GET /api/v2/sbom/compare` following the existing handler patterns (e.g., handlers for `/api/v2/sbom` and `/api/v2/advisory`). The handler should read `left` and `right` query parameters and return the fixture data. Add a handler that returns 400 if either parameter is missing.
- **Unit tests**: In `SbomComparePage.test.tsx`, use the test setup from `tests/setup.ts` with React Testing Library render helpers and MSW. Follow the testing patterns in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` for component mounting, route simulation, and assertion style.
- **E2E test**: In `tests/e2e/sbom-compare.spec.ts`, follow the pattern in `tests/e2e/sbom-list.spec.ts`. The test should:
  1. Navigate to `/sbom/compare`
  2. Verify the empty state is shown
  3. Select two SBOMs from the dropdowns
  4. Click the Compare button
  5. Verify all six diff sections render with expected content
  6. Verify the URL contains `left` and `right` query parameters
  7. Reload the page and verify the comparison re-renders from URL params (URL shareability)

## Reuse Candidates
- `tests/setup.ts` — Test setup with MSW server initialization and render helpers
- `tests/mocks/handlers.ts` — Existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` — Fixture format pattern reference
- `tests/mocks/fixtures/advisories.json` — Fixture format pattern reference
- `tests/e2e/sbom-list.spec.ts` — Playwright E2E test pattern reference
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Unit test pattern for page components

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` is registered and returns fixture data
- [ ] Mock fixture contains representative data for all six diff sections
- [ ] Unit tests pass and cover empty state, loading state, and populated state rendering
- [ ] E2E test passes the full comparison workflow: navigate, select, compare, verify, reload
- [ ] E2E test verifies URL shareability (comparison persists across page reload)

## Test Requirements
- [ ] Unit test: page renders empty state when navigated to without query params
- [ ] Unit test: page shows loading state while comparison is in progress
- [ ] Unit test: page renders all six diff sections with correct counts after comparison completes
- [ ] Unit test: Critical severity vulnerability row has highlighted styling
- [ ] E2E test: full comparison workflow from SBOM selection to diff rendering
- [ ] E2E test: URL-based comparison loads correctly on page reload

## Verification Commands
- `npx vitest run src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — E2E test passes

## Dependencies
- Depends on: Task 5 — Frontend comparison page
