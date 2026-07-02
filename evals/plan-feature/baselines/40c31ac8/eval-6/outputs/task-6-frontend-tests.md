## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add MSW request handlers for the remediation API endpoints and comprehensive component tests for the RemediationDashboard page. Create mock data fixtures for remediation responses and write tests covering rendering, loading states, data display, and filter interactions using Vitest and React Testing Library.

## Files to Create
- `src/pages/RemediationDashboard/RemediationDashboard.test.tsx` — Component tests for the dashboard page covering rendering, loading states, data display, and filter interactions
- `tests/mocks/fixtures/remediation.json` — Mock fixture data for remediation summary and by-product API responses

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
Follow the test patterns established in existing page test files.

- Add MSW handlers in `tests/mocks/handlers.ts` that return mock fixtures for both remediation endpoints
- Create realistic mock data: the fixture should include counts for all four severity levels (Critical, High, Medium, Low) and three statuses (Open, In Progress, Resolved); the by-product section should include at least 3 products with varying remediation progress
- Test cases for the dashboard page:
  - Renders summary cards with correct counts from mock data
  - Shows loading state while data is fetching
  - Shows empty state when no remediation data exists
  - Renders progress chart without errors
  - Renders RemediationTable with data rows
  - Filter interactions update the displayed data
- Use Vitest as the test runner and React Testing Library for component rendering and assertions
- Tests should verify that the correct API endpoints are called with expected parameters

Per CONVENTIONS.md §MSW Mocking: add request handlers in tests/mocks/handlers.ts. Applies: task modifies tests/mocks/handlers.ts matching the convention's .ts test mock scope.

## Acceptance Criteria
- [ ] MSW handlers registered for both remediation endpoints return mock fixtures
- [ ] Dashboard page test verifies summary cards render with correct counts
- [ ] Dashboard page test verifies loading and empty states
- [ ] Dashboard page test verifies RemediationTable renders data rows
- [ ] Dashboard page test verifies filter interactions
- [ ] Mock fixtures contain realistic data covering all severity levels and statuses
- [ ] All tests pass

## Test Requirements
- [ ] Test: summary cards display correct counts matching mock fixture values
- [ ] Test: loading state appears before data loads
- [ ] Test: empty state appears when API returns empty data
- [ ] Test: RemediationTable rows match by-product mock fixture entries
- [ ] Test: severity filter reduces displayed rows to matching severity
- [ ] Test: product filter reduces displayed rows to matching product

## Dependencies
- Depends on: Task 5 (dashboard page and components must exist to test)

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
