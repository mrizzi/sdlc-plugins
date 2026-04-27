# Task 7 — E2E tests for SBOM comparison workflow

## Repository
trustify-ui

## Description
Add Playwright end-to-end tests that exercise the full SBOM comparison workflow: selecting two SBOMs from the list page, navigating to the comparison page, verifying the diff sections render correctly, and testing URL-shareable comparisons. These tests verify the complete user journey described in UC-1 and UC-2 of the feature specification.

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW handlers for the `GET /api/v2/sbom/compare` endpoint
- `tests/mocks/fixtures/sboms.json` — add or extend mock SBOM data to support comparison scenarios (at least two SBOMs with known differences)

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for the comparison workflow
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response data with all six diff categories populated

## Implementation Notes
- Follow the existing E2E test pattern in `tests/e2e/sbom-list.spec.ts` — reference for Playwright test setup, page navigation, selector patterns, and assertion conventions.
- **MSW mock handler** for comparison endpoint: add a handler in `tests/mocks/handlers.ts` that intercepts `GET /api/v2/sbom/compare` and returns the fixture data from `tests/mocks/fixtures/sbom-comparison.json`. Follow the pattern of existing handlers in that file.
- **Mock fixture data**: create `tests/mocks/fixtures/sbom-comparison.json` with a complete `SbomComparisonResult` that includes entries in all six diff categories. Include at least one critical-severity vulnerability to test the highlighting behavior.
- **Test scenarios**:
  1. **Full comparison workflow (UC-1)**: navigate to SBOM list, select two SBOMs, click Compare, verify all six diff sections render with correct data
  2. **URL-shareable comparison (UC-2)**: navigate directly to `/sbom/compare?left=id1&right=id2`, verify the comparison loads automatically without manual selection
  3. **Empty state**: navigate to `/sbom/compare` without query params, verify the empty state message renders ("Select two SBOMs to compare")
  4. **Critical vulnerability highlighting**: verify that rows with critical severity in the New Vulnerabilities section have distinct visual styling
  5. **Section expand/collapse**: verify sections with items are expanded by default and can be collapsed
- **Selectors**: use PatternFly data attributes and ARIA roles for robust selectors (e.g., `role="row"`, `data-testid` attributes if added by components, PatternFly class patterns).

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` — existing E2E test for SBOM list page; follow the same Playwright patterns, navigation helpers, and assertion style
- `tests/mocks/handlers.ts` — existing MSW handlers; follow the pattern for adding new endpoint handlers
- `tests/mocks/fixtures/sboms.json` — existing SBOM fixture data; reference for fixture data format and ensure compatibility with comparison test scenarios
- `tests/setup.ts` — test setup including MSW server configuration; ensure new handlers are registered

## Acceptance Criteria
- [ ] E2E test covers the full comparison workflow from SBOM list selection through diff rendering
- [ ] E2E test covers direct URL navigation to a comparison (shareable URL)
- [ ] E2E test verifies empty state when no comparison is active
- [ ] E2E test verifies critical vulnerability rows have highlighted styling
- [ ] E2E test verifies diff sections are expandable/collapsible
- [ ] All E2E tests pass in CI-compatible headless mode
- [ ] MSW mock handlers return realistic comparison data

## Test Requirements
- [ ] E2E test: select two SBOMs from list page and navigate to comparison via "Compare selected" button
- [ ] E2E test: comparison page renders all six diff sections with correct data from mock
- [ ] E2E test: navigating to `/sbom/compare?left=id1&right=id2` auto-loads the comparison
- [ ] E2E test: `/sbom/compare` without params shows empty state
- [ ] E2E test: critical severity rows in New Vulnerabilities section are visually highlighted
- [ ] E2E test: expanding and collapsing diff sections works correctly

## Verification Commands
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — all E2E tests pass

## Dependencies
- Depends on: Task 5 — SBOM comparison page and routing
- Depends on: Task 6 — SBOM list page selection and compare navigation
