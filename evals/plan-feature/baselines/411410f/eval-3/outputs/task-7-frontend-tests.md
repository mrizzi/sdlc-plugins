# Task 7: Add MSW mocks, unit tests, and E2E test for SBOM comparison

## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive test coverage for the SBOM comparison feature: MSW mock handlers and fixture data for the comparison endpoint, unit tests for the comparison page component, and a Playwright E2E test that exercises the full comparison workflow from SBOM selection through diff rendering.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data with entries in all six diff categories
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare`

## Implementation Notes
- **Mock fixture** (`tests/mocks/fixtures/sbom-comparison.json`):
  - Create a realistic `SbomComparison` response with at least 2 entries per diff category.
  - Include a "critical" severity vulnerability in `new_vulnerabilities` to test the highlighted row styling.
  - Follow the JSON structure from the existing fixtures in `tests/mocks/fixtures/sboms.json` for style consistency.

- **MSW handler** (`tests/mocks/handlers.ts`):
  - Add a handler for `GET /api/v2/sbom/compare` that reads `left` and `right` query parameters.
  - Return the fixture data from `sbom-comparison.json`.
  - Add an error handler variant that returns 404 when invalid IDs are provided.
  - Follow the existing handler patterns in that file (e.g., the handlers for `/api/v2/sbom`).

- **Unit tests** (`SbomComparePage.test.tsx`):
  - Follow the testing pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` — use React Testing Library with the MSW server from `tests/setup.ts`.
  - Test cases:
    1. **Empty state rendering**: Render the page without query params, verify `EmptyState` component with "Select two SBOMs to compare" text is displayed.
    2. **Comparison results rendering**: Render the page with `left` and `right` query params, verify all six `ExpandableSection` diff sections render with correct titles and counts.
    3. **Loading state**: Verify `Skeleton` placeholders appear while the API call is pending.
    4. **Critical vulnerability highlighting**: Verify that rows in the New Vulnerabilities section with "critical" severity have the highlighted background class.
    5. **Badge colors**: Verify that `Badge` components use the correct color for each section (green for added/resolved, red for removed/new vulns, blue for version changes, yellow for license changes).
    6. **SeverityBadge usage**: Verify the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` is rendered in the New Vulnerabilities and Resolved Vulnerabilities sections.

- **E2E test** (`tests/e2e/sbom-compare.spec.ts`):
  - Follow the Playwright pattern in `tests/e2e/sbom-list.spec.ts`.
  - Test the full workflow:
    1. Navigate to the SBOM list page.
    2. Select two SBOMs using checkboxes.
    3. Click "Compare selected".
    4. Verify the URL changes to `/sbom/compare?left=...&right=...`.
    5. Verify the comparison page renders with diff sections.
    6. Expand a collapsed section and verify table content.
    7. Verify the page can be refreshed and the comparison reloads from URL params.

## Acceptance Criteria
- [ ] MSW handler for the comparison endpoint is registered and returns mock data
- [ ] Mock fixture contains realistic data with entries in all six diff categories
- [ ] At least 5 unit tests pass for the comparison page component
- [ ] E2E test exercises the full workflow from SBOM list selection to comparison rendering
- [ ] All tests pass in CI (`npm test` and `npx playwright test`)
- [ ] No existing tests are broken by the new test additions

## Test Requirements
- [ ] Unit test: empty state renders when no comparison is active
- [ ] Unit test: all six diff sections render with correct data from mock
- [ ] Unit test: loading skeleton appears during API fetch
- [ ] Unit test: critical vulnerability rows are visually highlighted
- [ ] Unit test: SeverityBadge is used for vulnerability severity display
- [ ] E2E test: full comparison workflow from SBOM list to diff rendering
- [ ] E2E test: URL shareability (refresh preserves comparison state)

## Dependencies
- Depends on: Task 5 — Build the SBOM comparison page UI
- Depends on: Task 6 — Add comparison selection to SBOM list page
