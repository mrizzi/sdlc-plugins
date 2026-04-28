# Task 7 -- Frontend Comparison Tests, MSW Handlers, and E2E Test

## Repository
trustify-ui

## Description
Add comprehensive test coverage for the SBOM comparison feature: MSW mock handlers and fixture data for the comparison API, unit tests for comparison page components, and a Playwright E2E test that exercises the full comparison workflow from SBOM selection through diff rendering.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` -- mock comparison API response with representative data across all six diff categories
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests for the comparison page component
- `tests/e2e/sbom-compare.spec.ts` -- Playwright E2E test for the full comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW request handler for `GET /api/v2/sbom/compare` returning the mock comparison fixture

## Implementation Notes
- Follow the existing test patterns:
  - Unit tests: Vitest + React Testing Library pattern as seen in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`.
  - MSW handlers: follow the handler pattern in `tests/mocks/handlers.ts` for intercepting API calls.
  - Fixtures: follow the data structure in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for mock data format.
  - E2E tests: follow the Playwright pattern in `tests/e2e/sbom-list.spec.ts`.
- The mock comparison fixture should include at least: 2 added packages, 2 removed packages, 1 version change (upgrade), 1 version change (downgrade), 1 new critical vulnerability, 1 new medium vulnerability, 1 resolved vulnerability, and 1 license change. This ensures all diff sections and visual states are testable.
- Unit test coverage should include:
  - Empty state rendering (no query params)
  - Loading state (skeleton display)
  - Full comparison rendering with all six sections
  - Critical vulnerability row highlighting
  - Section expand/collapse behavior
  - URL parameter handling (pre-populated selectors from query params)
- E2E test should cover UC-1: navigate to SBOM list, select two SBOMs, click Compare, verify all diff sections render with expected data.
- Use the existing test setup in `tests/setup.ts` for MSW and render helpers.

## Reuse Candidates
- `tests/mocks/handlers.ts` -- existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` -- mock data format reference for creating comparison fixtures
- `tests/mocks/fixtures/advisories.json` -- mock advisory data format reference
- `tests/setup.ts` -- test setup with MSW and render helpers
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- unit test pattern for page components
- `tests/e2e/sbom-list.spec.ts` -- E2E test pattern with Playwright

## Acceptance Criteria
- [ ] MSW handler intercepts comparison API calls and returns mock data
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] Unit tests cover empty state, loading state, and full comparison rendering
- [ ] Unit tests verify critical vulnerability row highlighting
- [ ] E2E test exercises the full workflow: list page selection, compare navigation, diff rendering
- [ ] All tests pass

## Test Requirements
- [ ] Unit test: empty state renders when no comparison query params are present
- [ ] Unit test: skeleton loading state renders while API call is in progress
- [ ] Unit test: all six diff sections render with correct data from mock response
- [ ] Unit test: critical severity vulnerability rows have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: URL query params pre-populate the SBOM selectors
- [ ] E2E test: select two SBOMs from the list page, click Compare, verify diff sections appear with correct data

## Dependencies
- Depends on: Task 5 -- Frontend SBOM Comparison Page
- Depends on: Task 6 -- Frontend SBOM List Page Selection and Compare Navigation
