## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW mock handlers and test fixtures for the SBOM comparison endpoint, and add a Playwright E2E test for the comparison workflow (select two SBOMs, click Compare, verify diff sections render).

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison result fixture with sample data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock comparison fixture
- `tests/setup.ts` — Ensure the new handler is registered in the MSW server setup

## Implementation Notes
Follow the existing MSW mock pattern in `tests/mocks/handlers.ts` — add a handler for `GET /api/v2/sbom/compare` that reads `left` and `right` query params and returns the fixture from `tests/mocks/fixtures/sbom-comparison.json`.

The fixture in `tests/mocks/fixtures/sbom-comparison.json` should include at least one entry in each of the six diff categories to enable comprehensive rendering tests. Follow the fixture patterns in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`.

The Playwright E2E test in `tests/e2e/sbom-compare.spec.ts` should follow the pattern in `tests/e2e/sbom-list.spec.ts`. Test the full workflow:
1. Navigate to the SBOM list page
2. Select two SBOMs
3. Click "Compare selected"
4. Verify the comparison page loads with diff sections
5. Verify at least one diff section shows data

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW request handlers pattern to follow
- `tests/mocks/fixtures/sboms.json` — Mock SBOM data fixture pattern to follow
- `tests/mocks/fixtures/advisories.json` — Mock advisory data fixture pattern to follow
- `tests/e2e/sbom-list.spec.ts` — Playwright E2E test pattern to follow
- `tests/setup.ts` — Test setup with MSW handler registration

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` returns mock comparison data
- [ ] Mock fixture includes sample entries in all six diff categories
- [ ] E2E test navigates from SBOM list to comparison page and verifies diff sections
- [ ] All existing tests continue to pass after adding the new handler

## Test Requirements
- [ ] E2E test: select two SBOMs from the list, click Compare, verify comparison page renders with diff sections
- [ ] E2E test: verify URL contains `left` and `right` query params after comparison
- [ ] E2E test: verify at least one diff section contains data rows

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Frontend comparison page UI

[sdlc-workflow] Description digest: sha256-md:3799639b6ecce30f0df25c2e4f63e70dc08b7d75b4a24c93d036e41e2e854156
