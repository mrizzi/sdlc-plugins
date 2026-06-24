## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive tests for the SBOM comparison feature: MSW mock handlers for the comparison endpoint, unit tests for the comparison page and its sub-components, and a Playwright E2E test for the full comparison workflow.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison API response data
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare`

## Implementation Notes
**MSW handler** in `tests/mocks/handlers.ts`:
Add a new handler following the pattern of existing handlers in that file. The handler should intercept `GET /api/v2/sbom/compare` requests and return the fixture data from `tests/mocks/fixtures/sbom-comparison.json`.

**Mock fixture** `tests/mocks/fixtures/sbom-comparison.json`:
Create a realistic comparison response with entries in all six diff categories. Include at least one critical-severity vulnerability in `new_vulnerabilities` to test the highlighted row styling.

**Unit tests** in `SbomComparePage.test.tsx`:
Follow the testing pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` using Vitest + React Testing Library.
- Test empty state rendering when no query params
- Test loading state when query params are present but data is loading
- Test full comparison rendering with mock data
- Test that Critical severity rows have highlighted styling
- Test Export dropdown renders with JSON and CSV options
- Test that SBOM selectors are populated

**E2E test** in `tests/e2e/sbom-compare.spec.ts`:
Follow the pattern in `tests/e2e/sbom-list.spec.ts` using Playwright.
- Navigate to SBOM list page
- Select two SBOMs via checkboxes
- Click "Compare selected"
- Verify comparison page loads with diff sections
- Verify URL contains both SBOM IDs
- Verify expanding a diff section shows table data

Per Key Conventions (Testing): Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking. Applies: task creates test files and modifies `tests/mocks/handlers.ts` matching the convention's testing scope.

## Acceptance Criteria
- [ ] MSW handler intercepts comparison API requests and returns fixture data
- [ ] Unit tests cover empty state, loading state, and populated comparison view
- [ ] Unit tests verify Critical severity row highlighting
- [ ] E2E test covers full comparison workflow from SBOM list to comparison view
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Unit test: empty state renders when no query params
- [ ] Unit test: loading skeletons appear during data fetch
- [ ] Unit test: all six diff sections render with correct counts
- [ ] Unit test: Critical severity vulnerability rows are highlighted
- [ ] Unit test: Export dropdown contains JSON and CSV options
- [ ] E2E test: full comparison workflow from list page to comparison results

## Verification Commands
```bash
npx vitest run src/pages/SbomComparePage/
npx playwright test tests/e2e/sbom-compare.spec.ts
```

## Dependencies
- Depends on: Task 7 — SBOM comparison page component
- Depends on: Task 9 — SBOM list page compare action

[sdlc-workflow] Description digest: sha256-md:9bf236e3d9957baaea2d3f470f7c05cbbb5d8facc75d7df168005e4900ccbab3
