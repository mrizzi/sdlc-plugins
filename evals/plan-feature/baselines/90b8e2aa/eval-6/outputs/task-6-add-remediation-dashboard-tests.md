## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive test coverage for the remediation dashboard: unit tests with React Testing Library and MSW mock handlers for component behavior, and Playwright E2E tests for the full user workflow including navigation, filtering, and data display.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page: renders summary cards, displays table data, applies filters, handles loading and empty states
- `tests/mocks/fixtures/remediation.json` — mock remediation data with known severity/status/product values for deterministic test assertions
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E tests: navigate to /remediation, verify summary cards render, apply severity filter, apply product filter, verify table updates

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` returning mock fixture data

## Implementation Notes
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking. Follow the testing patterns established in existing page tests.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's TypeScript test file scope.
- Per CONVENTIONS.md §Testing setup: MSW handlers are defined in `tests/mocks/handlers.ts` and fixtures in `tests/mocks/fixtures/`. See `tests/mocks/handlers.ts` for the established handler pattern and `tests/mocks/fixtures/sboms.json` for fixture data format.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's TypeScript test mock scope.
- Per CONVENTIONS.md §Naming: use kebab-case for test fixture files and E2E spec files.
  Applies: task creates `tests/e2e/remediation-dashboard.spec.ts` matching the convention's TypeScript E2E test file scope.
- Mock data should include multiple products with varying severity distributions to exercise all filter combinations.
- E2E tests should cover the UC-1 and UC-2 user workflows from the feature description.
- Use `tests/setup.ts` render helpers for unit test setup.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW request handlers; extend with remediation endpoint handlers following the same pattern
- `tests/mocks/fixtures/sboms.json` — mock SBOM data fixture; reference for fixture data structure and format
- `tests/mocks/fixtures/advisories.json` — mock advisory data fixture; reference for fixture data with severity fields
- `tests/setup.ts` — test setup with MSW handlers and render helpers; reuse for remediation test setup
- `src/pages/SbomListPage/SbomListPage.test.tsx` — existing page unit test; reference for testing patterns with RTL and MSW
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test; reference for E2E test structure and navigation patterns

## Acceptance Criteria
- [ ] Unit tests verify summary cards render with correct counts from mock data
- [ ] Unit tests verify vulnerability table renders rows from mock data
- [ ] Unit tests verify severity filter narrows table results
- [ ] Unit tests verify product filter narrows table results
- [ ] Unit tests verify loading state is displayed during data fetch
- [ ] Unit tests verify empty state is displayed when API returns no data
- [ ] MSW handlers return deterministic mock data for both remediation endpoints
- [ ] E2E test navigates to `/remediation` and verifies dashboard loads
- [ ] E2E test applies a severity filter and verifies table updates
- [ ] E2E test applies a product filter and verifies dashboard shows product-specific data

## Test Requirements
- [ ] Unit tests achieve coverage for all RemediationDashboardPage component branches
- [ ] Unit tests cover SummaryCards, RemediationChart, and VulnerabilityTable sub-components
- [ ] E2E tests cover UC-1 (view remediation summary) and UC-2 (filter by product) user workflows
- [ ] All tests pass with `npm test` and `npx playwright test`

## Verification Commands
- `npm test -- --reporter=verbose RemediationDashboardPage` — all unit tests pass
- `npx playwright test tests/e2e/remediation-dashboard.spec.ts` — all E2E tests pass

## Dependencies
- Depends on: Task 5 — Add remediation dashboard page
