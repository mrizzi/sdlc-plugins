## Repository
trustify-ui

## Description
Add MSW mock handlers, fixture data, and an E2E test for the SBOM comparison workflow. This provides API-level mocking for unit tests across the comparison feature and a Playwright end-to-end test covering the full user flow from SBOM selection through comparison rendering.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison API response fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test covering the comparison workflow (UC-1)

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the fixture data

## Implementation Notes
**MSW handler** — add to `tests/mocks/handlers.ts` following the pattern of existing handlers in that file. The handler should:
1. Match `GET /api/v2/sbom/compare` requests
2. Extract `left` and `right` query parameters
3. Return the `sbom-comparison.json` fixture data as the response
4. Handle error cases: return 400 if parameters are missing, 404 for unknown IDs

**Fixture data** — create `tests/mocks/fixtures/sbom-comparison.json` following the pattern of existing fixtures in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`. Include:
- 2-3 added packages (one with advisory_count > 0)
- 2-3 removed packages
- 1-2 version changes (one upgrade, one downgrade)
- 2-3 new vulnerabilities (at least one with severity "critical" to test highlighting)
- 1-2 resolved vulnerabilities
- 1-2 license changes

**E2E test** — create `tests/e2e/sbom-compare.spec.ts` following the pattern in `tests/e2e/sbom-list.spec.ts`. The test should cover the full UC-1 flow:
1. Navigate to the SBOM list page
2. Select two SBOMs using checkboxes
3. Click "Compare selected"
4. Verify navigation to `/sbom/compare?left=...&right=...`
5. Verify the comparison page renders with diff sections
6. Verify the count badges show correct numbers
7. Verify Critical severity rows in New Vulnerabilities have highlighted styling
8. Test URL shareability: navigate directly to a comparison URL and verify it loads the comparison

**PatternFly component assertions** — use PatternFly-specific selectors for assertions:
- `ExpandableSection` sections by their toggle button text
- `Badge` count values
- `Table` row counts per section
- `SeverityBadge` rendered text for vulnerability severity

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers; follow the same pattern for the new comparison endpoint
- `tests/mocks/fixtures/sboms.json` — existing SBOM fixture; reference for mock data structure
- `tests/mocks/fixtures/advisories.json` — existing advisory fixture; reference for advisory mock data
- `tests/e2e/sbom-list.spec.ts` — existing E2E test; follow the same Playwright patterns and page navigation conventions
- `tests/setup.ts` — test setup with MSW server initialization; ensure the new handler is registered

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint is registered and returns fixture data
- [ ] Fixture data includes representative items in all six diff categories
- [ ] E2E test covers the full comparison workflow from SBOM list to comparison view
- [ ] E2E test verifies URL shareability (direct navigation to comparison URL)
- [ ] E2E test verifies Critical severity highlighting
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] MSW handler returns correct fixture data for valid comparison requests
- [ ] MSW handler returns 400 for missing parameters
- [ ] E2E test: select two SBOMs and navigate to comparison page
- [ ] E2E test: verify all six diff sections render with correct data
- [ ] E2E test: verify count badges display correct numbers
- [ ] E2E test: verify direct URL navigation loads comparison without re-selection
- [ ] E2E test: verify Critical severity rows are visually highlighted

## Verification Commands
- `npx vitest run` — run unit tests, expected: all pass including new comparison tests
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — run comparison E2E test, expected: passes

## Dependencies
- Depends on: Task 5 — Frontend comparison page
- Depends on: Task 6 — Frontend SBOM list selection
