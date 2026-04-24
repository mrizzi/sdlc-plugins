## Repository
trustify-ui

## Description
Add comprehensive test coverage for the SBOM comparison page (TC-9003): MSW mock handlers and fixtures for the comparison endpoint, unit tests for the comparison page component, and a Playwright E2E test covering the full comparison workflow. This ensures the comparison feature works correctly at both the component and end-to-end levels.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` that returns mock comparison data

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture with sample data across all six diff categories
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component using Vitest and React Testing Library
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Implementation Notes
- **MSW handler**: Follow the existing handler pattern in `tests/mocks/handlers.ts` — add a `rest.get("/api/v2/sbom/compare", ...)` handler that reads `left` and `right` query params and returns the fixture data. Return 400 if either param is missing. Return 404 for a specific "nonexistent" ID to support error case testing.
- **Mock fixture**: The `sbom-comparison.json` fixture should include sample entries in all six diff categories to enable comprehensive testing: at least 2 added packages, 2 removed packages, 1 version change (upgrade), 1 version change (downgrade), 1 critical vulnerability, 1 non-critical vulnerability, 1 resolved vulnerability, and 1 license change.
- **Unit tests**: Follow the testing pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` — use Vitest with React Testing Library and the MSW server from `tests/setup.ts`.
- **Unit test scenarios**:
  - Render the page without query params and verify the empty state is displayed
  - Render the page with valid query params and mock data, verify all six diff sections render with correct counts
  - Verify that the "Compare" button is disabled when only one SBOM is selected
  - Verify critical vulnerability rows have highlighted styling
  - Verify loading state shows skeleton placeholders
- **E2E test**: Follow the Playwright pattern in `tests/e2e/sbom-list.spec.ts`. The E2E test should:
  1. Navigate to `/sbom/compare`
  2. Verify the empty state is displayed
  3. Select two SBOMs from the selectors
  4. Click "Compare"
  5. Verify the URL updates with query params
  6. Verify all six diff sections appear with data
  7. Navigate directly to a comparison URL with query params and verify it loads correctly (shareable URL test)

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW handler patterns for reference
- `tests/mocks/fixtures/sboms.json` — Existing fixture format for reference
- `tests/mocks/fixtures/advisories.json` — Existing fixture format for advisory data reference
- `tests/setup.ts` — Test setup with MSW server and render helpers
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Reference for page-level unit test patterns
- `tests/e2e/sbom-list.spec.ts` — Reference for Playwright E2E test patterns

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` returns mock data for valid requests and appropriate errors for invalid ones
- [ ] Mock fixture contains sample data for all six diff categories
- [ ] Unit tests pass for empty state, loaded state, loading state, compare button disabled state, and critical vulnerability highlighting
- [ ] E2E test passes for the full comparison workflow including SBOM selection, comparison execution, URL sharing, and result display
- [ ] All existing tests continue to pass (no regressions from new mock handlers)

## Test Requirements
- [ ] Unit test: empty state renders when no query params are present
- [ ] Unit test: all six diff sections render with correct item counts when comparison data is loaded
- [ ] Unit test: compare button is disabled when only one SBOM selector has a value
- [ ] Unit test: critical vulnerability rows display with highlighted background
- [ ] Unit test: loading state shows skeleton placeholders in diff sections
- [ ] E2E test: full comparison workflow from page load to result display
- [ ] E2E test: navigating to a shareable comparison URL loads the correct comparison

## Dependencies
- Depends on: Task 5 — Frontend comparison page UI
