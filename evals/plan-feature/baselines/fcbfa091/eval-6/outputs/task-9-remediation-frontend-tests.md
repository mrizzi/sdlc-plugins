## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add unit tests, MSW mock handlers, mock fixtures, and a Playwright E2E test for the remediation dashboard. Tests cover the dashboard page rendering, summary cards, filterable table interactions, and end-to-end navigation flow.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Unit tests for the dashboard page component
- `tests/mocks/fixtures/remediation-summary.json` — Mock fixture for remediation summary API response
- `tests/mocks/fixtures/remediation-by-product.json` — Mock fixture for per-product remediation API response
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E test for remediation dashboard navigation and interaction

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
Follow the testing patterns from existing test files:

Per CONVENTIONS.md: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.tsx` test file scope.

Per CONVENTIONS.md: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
Applies: task creates `tests/e2e/remediation-dashboard.spec.ts` matching the convention's `.ts` test file scope.

For MSW handlers (`tests/mocks/handlers.ts`):
- Add `rest.get("/api/v2/remediation/summary", ...)` returning the mock summary fixture
- Add `rest.get("/api/v2/remediation/by-product", ...)` returning the mock by-product fixture
- Follow the existing handler patterns in the file

For mock fixtures:
- `remediation-summary.json`: Include data with all four severity levels and all three statuses, with realistic counts
- `remediation-by-product.json`: Include 3-5 mock products with varying remediation counts

For unit tests (`RemediationDashboardPage.test.tsx`):
- Reference `src/pages/SbomListPage/SbomListPage.test.tsx` for test setup patterns
- Test: page renders summary cards with correct counts from mock data
- Test: page renders chart component
- Test: loading spinner appears before data loads
- Test: empty state appears when no data
- Test: filter toolbar renders with severity/product/status options
- Test: filtering updates the vulnerability table

For E2E test (`remediation-dashboard.spec.ts`):
- Reference `tests/e2e/sbom-list.spec.ts` for E2E test patterns
- Test: navigate to `/remediation` from the main navigation
- Test: summary cards are visible with data
- Test: apply a severity filter and verify table updates
- Test: pagination controls work

## Reuse Candidates
- `tests/setup.ts` — Test setup with MSW handlers and render helpers; use for unit test configuration
- `tests/mocks/handlers.ts` — Existing MSW handlers to extend with remediation endpoints
- `tests/mocks/fixtures/sboms.json` — Reference for mock fixture structure
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Reference for page component unit test patterns
- `tests/e2e/sbom-list.spec.ts` — Reference for Playwright E2E test patterns

## Acceptance Criteria
- [ ] MSW handlers intercept remediation API requests and return mock data
- [ ] Unit tests verify summary cards render with correct counts
- [ ] Unit tests verify loading and empty states
- [ ] Unit tests verify filter interactions update the table
- [ ] E2E test navigates to remediation dashboard and verifies page content
- [ ] E2E test exercises filter interactions
- [ ] All tests pass with `npm test` and `npx playwright test`

## Test Requirements
- [ ] Unit test: summary cards display correct open/in-progress/resolved counts
- [ ] Unit test: loading spinner shown during data fetch
- [ ] Unit test: empty state shown when no remediation data exists
- [ ] Unit test: severity filter updates displayed vulnerabilities
- [ ] E2E test: navigate to /remediation from sidebar navigation
- [ ] E2E test: summary cards visible with data
- [ ] E2E test: filter by Critical severity and verify table update
- [ ] E2E test: pagination controls navigate between pages

## Verification Commands
- `npm test -- --run RemediationDashboardPage` — Unit tests pass
- `npx playwright test remediation-dashboard` — E2E test passes

## Dependencies
- Depends on: Task 7 — Vulnerability table component
- Depends on: Task 8 — Routing and navigation

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
