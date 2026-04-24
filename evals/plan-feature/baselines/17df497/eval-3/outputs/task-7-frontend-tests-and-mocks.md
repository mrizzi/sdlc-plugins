# Task 7 — Frontend E2E tests and MSW handlers for comparison feature

## Repository
trustify-ui

## Description
Add MSW (Mock Service Worker) request handlers for the SBOM comparison endpoint, mock fixture data for comparison results, and Playwright E2E tests covering the full comparison workflow: selecting two SBOMs from the list, navigating to the comparison page, viewing diff sections, and verifying URL-shareable behavior.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns mock comparison data

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock `SbomComparisonResult` fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for the comparison workflow

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` — existing handlers use `rest.get()` with typed response bodies.
- The mock fixture in `tests/mocks/fixtures/sbom-comparison.json` should include entries in all six diff categories so that E2E tests can verify all sections render correctly. Include at least one Critical severity vulnerability to test the highlighting behavior.
- Follow the Playwright E2E test pattern in `tests/e2e/sbom-list.spec.ts` for test structure, page navigation, and assertion patterns.
- The E2E test should cover the full UC-1 workflow: navigate to SBOM list, select two SBOMs, click "Compare selected", verify the comparison page loads with all diff sections.
- Test URL-shareability (UC-2): navigate directly to `/sbom/compare?left={id1}&right={id2}` and verify the comparison loads without manual selection.
- Follow the existing test setup in `tests/setup.ts` for MSW server initialization and render helpers.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data (use SBOM IDs from here for comparison test)
- `tests/mocks/fixtures/advisories.json` — existing mock advisory data for vulnerability test entries
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test patterns
- `tests/setup.ts` — test setup helpers

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` returns mock comparison data with correct query param handling
- [ ] Mock fixture includes entries in all six diff categories
- [ ] Mock fixture includes at least one Critical severity vulnerability entry
- [ ] E2E test covers selecting two SBOMs from list and navigating to comparison page
- [ ] E2E test verifies all six diff sections render with expected data
- [ ] E2E test verifies direct URL navigation loads comparison without manual selection
- [ ] E2E test verifies Critical vulnerability rows have highlighted styling
- [ ] E2E test verifies empty state when navigating to comparison page without query params

## Test Requirements
- [ ] E2E test: full comparison workflow from SBOM list selection through diff display
- [ ] E2E test: direct URL navigation with `left` and `right` params loads comparison
- [ ] E2E test: comparison page without params shows empty state
- [ ] E2E test: diff sections display correct counts in badges
- [ ] E2E test: Critical severity vulnerability row has visual emphasis

## Verification Commands
- `npx playwright test sbom-compare` — all comparison E2E tests pass
- `npx vitest run` — all unit tests pass including new MSW handlers

## Dependencies
- Depends on: Task 5 — Frontend SBOM Comparison Page
- Depends on: Task 6 — Frontend SBOM list page selection and compare navigation
