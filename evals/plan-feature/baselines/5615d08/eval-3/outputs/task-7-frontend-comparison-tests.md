## Repository
trustify-ui

## Description
Add MSW mock handlers and unit/E2E tests for the SBOM comparison feature. This ensures the comparison page, API hook, and list page selection behavior are all properly tested with mock data covering the full range of diff scenarios.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture with representative data for all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the full comparison workflow: select SBOMs from list, navigate to comparison, verify diff sections

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture data

## Implementation Notes
- In `tests/mocks/handlers.ts`, add a new `rest.get('/api/v2/sbom/compare', ...)` handler following the pattern of existing handlers in that file. The handler should read `left` and `right` query params and return the `sbom-comparison.json` fixture. Return 400 if either param is missing.
- The `sbom-comparison.json` fixture should include at least: 2 added packages, 1 removed package, 2 version changes (one upgrade, one downgrade), 2 new vulnerabilities (one critical, one medium), 1 resolved vulnerability, and 1 license change. This ensures all diff sections and edge cases are covered.
- In `SbomComparePage.test.tsx`, follow the testing pattern from `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`. Use React Testing Library with the render helpers from `tests/setup.ts`.
- For E2E tests in `tests/e2e/sbom-compare.spec.ts`, follow the pattern in `tests/e2e/sbom-list.spec.ts`. The E2E test should:
  1. Navigate to the SBOM list page
  2. Select two SBOMs via checkboxes
  3. Click "Compare selected"
  4. Verify the comparison page loads with diff sections
  5. Verify the URL contains both SBOM IDs
  6. Verify expanding/collapsing diff sections works

## Reuse Candidates
- `tests/setup.ts` — Reuse test setup, render helpers, and MSW server configuration
- `tests/mocks/handlers.ts` — Extend with the new comparison endpoint handler
- `tests/mocks/fixtures/sboms.json` — Reference for fixture format; the comparison fixture should use consistent SBOM IDs
- `tests/e2e/sbom-list.spec.ts` — Follow the same Playwright test structure and patterns
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Follow the same React Testing Library patterns

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint returns mock data for valid requests and 400 for invalid ones
- [ ] Unit tests pass for the comparison page covering empty state, loaded state, and error state
- [ ] E2E test passes for the full comparison workflow
- [ ] Mock fixture covers all six diff categories with realistic data

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params are present
- [ ] Unit test: comparison page renders all six diff sections with correct data from mock fixture
- [ ] Unit test: critical vulnerability row has highlighted styling
- [ ] Unit test: Export dropdown is disabled before comparison and enabled after
- [ ] E2E test: full workflow from SBOM list selection to comparison view verification
- [ ] E2E test: URL contains correct query parameters after comparison

## Dependencies
- Depends on: Task 5 — SBOM comparison page
- Depends on: Task 6 — SBOM list page compare action
