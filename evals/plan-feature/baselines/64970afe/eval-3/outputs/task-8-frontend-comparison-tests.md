## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add unit tests (Vitest + React Testing Library) and end-to-end tests (Playwright) for the SBOM comparison page, including MSW mock handlers for the comparison endpoint. Tests should cover the full user workflow: empty state, selecting SBOMs, triggering comparison, viewing results across all diff sections, and URL shareability.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests: empty state rendering, comparison result rendering for all diff sections, loading state, URL parameter pre-population, error state
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data with all six diff categories populated for test assertions
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests: navigate to SBOM list, select two SBOMs, click Compare, verify comparison page renders with results, test URL shareability

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` that returns mock comparison data from the fixture file

## Implementation Notes
- Follow the unit test pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` for component test structure, render helpers, and assertion patterns.
  Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's TypeScript test file scope.
- Use the test setup from `tests/setup.ts` for MSW initialization and render helpers.
- The mock fixture in `tests/mocks/fixtures/sbom-comparison.json` should contain representative data for all six diff categories (at least 1-2 items each) to verify each section renders correctly.
- Reference existing mock fixtures in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for fixture format patterns.
- MSW handler in `tests/mocks/handlers.ts` should intercept `GET */api/v2/sbom/compare*` and return the mock fixture data.
- E2E tests in `tests/e2e/sbom-compare.spec.ts` should follow the pattern in `tests/e2e/sbom-list.spec.ts` for Playwright test structure and selectors.
- Per CONVENTIONS.md §Naming: PascalCase for component files (SbomComparePage.test.tsx), kebab-case for test spec files (sbom-compare.spec.ts).
  Applies: task creates `tests/e2e/sbom-compare.spec.ts` matching the convention's test file naming scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — existing page unit test; follow the same testing patterns
- `tests/setup.ts` — existing test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handlers; extend with comparison endpoint handler
- `tests/mocks/fixtures/sboms.json` — existing SBOM mock data; reference for fixture format
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test; follow for E2E test structure

## Acceptance Criteria
- [ ] Unit tests pass for the SbomComparePage component
- [ ] MSW handler correctly intercepts comparison API requests and returns mock data
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] E2E tests pass the full comparison workflow (select, compare, verify results)
- [ ] Tests cover empty state, loading state, results state, and error state

## Test Requirements
- [ ] Unit test: renders empty state (EmptyState with CodeBranchIcon) when no comparison is active
- [ ] Unit test: renders loading skeletons when comparison is in progress
- [ ] Unit test: renders all six diff sections with correct data from mock response
- [ ] Unit test: renders Critical vulnerability rows with highlighted background
- [ ] Unit test: pre-populates SBOM selectors from URL query params
- [ ] Unit test: handles API error state gracefully
- [ ] E2E test: navigate to SBOM list, select two SBOMs, click Compare, verify redirect to comparison page
- [ ] E2E test: comparison page renders diff sections with data
- [ ] E2E test: loading comparison page via direct URL with query params shows results

## Verification Commands
- `npx vitest run src/pages/SbomComparePage/` — unit tests pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — E2E tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Implement SBOM comparison page with diff sections
- Depends on: Task 7 — Add route registration and SBOM list page compare trigger
