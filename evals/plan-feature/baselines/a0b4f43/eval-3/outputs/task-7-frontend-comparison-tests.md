## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive test coverage for the SBOM comparison feature: MSW request handlers and mock fixtures for the comparison endpoint, and a Playwright E2E test for the full comparison workflow from SBOM selection through diff display.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit/integration tests for the comparison page component
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` returning mock comparison data
- `tests/mocks/fixtures/sboms.json` — Add or extend with two SBOM entries that can serve as left/right comparison targets

## Implementation Notes
- Follow the existing test patterns:
  - Unit tests use Vitest + React Testing Library, as established in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`.
  - MSW handlers in `tests/mocks/handlers.ts` — add a handler for `GET */api/v2/sbom/compare*` that returns a fixture response.
  - E2E tests use Playwright, following the pattern in `tests/e2e/sbom-list.spec.ts`.
- Create a mock comparison fixture with representative data: at least 2 added packages, 1 removed package, 1 version change, 1 new vulnerability (with Critical severity for highlight testing), 1 resolved vulnerability, and 1 license change.
- The E2E test should exercise the full workflow:
  1. Navigate to the SBOM list page
  2. Select two SBOMs using checkboxes
  3. Click "Compare selected"
  4. Verify the comparison page loads with both SBOM selectors populated
  5. Verify diff sections appear with correct counts
  6. Verify URL contains both SBOM IDs (shareable URL)
- Unit tests for the page component should:
  - Render the empty state when no comparison has been triggered
  - Render all six diff sections with data from the MSW mock
  - Verify Critical severity rows in New Vulnerabilities have the highlighted style
  - Verify expanded/collapsed state of sections based on item count

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW handlers; follow the pattern for adding new API mock handlers
- `tests/mocks/fixtures/sboms.json` — Existing mock SBOM data; extend with entries suitable for comparison testing
- `tests/setup.ts` — Test setup with MSW server and render helpers; use for all new tests
- `tests/e2e/sbom-list.spec.ts` — Existing Playwright E2E test; follow its pattern for page navigation, element selection, and assertions
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Existing page test; follow its pattern for component rendering and query assertion

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint returns well-structured mock data
- [ ] Unit tests cover empty state, loaded state with all six diff sections, and Critical severity highlighting
- [ ] E2E test exercises the full comparison workflow from SBOM list selection through diff display
- [ ] E2E test verifies URL shareability (query params present after comparison)
- [ ] All tests pass in CI

## Test Requirements
- [ ] Unit test: page renders empty state with CodeBranchIcon and instructional text
- [ ] Unit test: page renders all six diff sections with correct item counts from mock data
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted background
- [ ] E2E test: full comparison workflow — select 2 SBOMs, click Compare, verify diff sections and URL params

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 6 — Create SBOM comparison page with diff sections and routing (trustify-ui)