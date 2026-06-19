## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive tests for the SBOM comparison page and set up MSW mock handlers and fixtures for the comparison endpoint. This task creates the mock data fixtures, adds MSW request handlers for the comparison API, and writes component tests that verify the full user workflow (selecting SBOMs, triggering comparison, verifying rendered diff sections).

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data with representative entries in all six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes)
- `src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` — Component tests for the comparison page using React Testing Library

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock comparison fixture

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` — use `rest.get()` with the comparison endpoint path and return the fixture JSON.
- Follow the existing fixture pattern in `tests/mocks/fixtures/sboms.json` — create realistic mock data with multiple entries per diff category.
- Follow the existing test pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` — use `render()` from React Testing Library with appropriate providers (React Query, React Router).
- The mock fixture should include:
  - At least 2 added packages (one with advisories)
  - At least 2 removed packages
  - At least 1 version change (upgrade) and 1 version change (downgrade)
  - At least 2 new vulnerabilities (one with "critical" severity to test row highlighting)
  - At least 1 resolved vulnerability
  - At least 1 license change
- Tests should use `screen.getByText()` and `screen.getByRole()` for assertions per React Testing Library best practices.
- Test the URL query parameter flow by providing initial route with `?left=id1&right=id2` to verify auto-loading.
- Use `waitFor()` for async assertions after API calls complete.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handler registration pattern
- `tests/mocks/fixtures/sboms.json` — fixture format reference
- `tests/setup.ts` — test setup configuration and render helpers
- `src/pages/SbomListPage/SbomListPage.test.tsx` — component test pattern with React Testing Library

## Dependencies
- Depends on: Task 5 — Frontend comparison page (component being tested)

## Acceptance Criteria
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` and returns mock fixture data
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] Component tests pass and cover the core user workflows
- [ ] Tests verify empty state rendering on initial load
- [ ] Tests verify diff section rendering after comparison is triggered
- [ ] Tests verify critical severity row highlighting in New Vulnerabilities section

## Test Requirements
- [ ] Component test: page renders empty state when loaded without query params
- [ ] Component test: page auto-loads comparison when URL contains `left` and `right` query params
- [ ] Component test: all six diff sections render with correct item counts from mock data
- [ ] Component test: expandable sections with items are expanded, empty sections are collapsed
- [ ] Component test: critical severity vulnerability row has highlighted style
- [ ] Component test: Export dropdown is enabled after comparison loads

## Verification Commands
- `npx vitest run src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` — all comparison page tests pass
