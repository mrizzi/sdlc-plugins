# Task 8 — Add E2E tests for SBOM comparison workflow

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add Playwright end-to-end tests covering the full SBOM comparison workflow: selecting two SBOMs from the list page, clicking Compare, verifying the comparison page renders correctly with all diff sections, and verifying URL-shareable comparisons.

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test suite for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` if not already added by Task 5
- `tests/mocks/fixtures/comparison.json` — Add mock comparison response fixture data (if not already created by Task 6)

## Implementation Notes
- Follow the existing E2E test pattern in `tests/e2e/sbom-list.spec.ts` — use Playwright's page object pattern, test selectors, and assertion style.
- Test scenarios should cover:
  1. Navigate to SBOM list, select two SBOMs, click "Compare selected", verify navigation to comparison page
  2. Verify comparison page renders all six diff sections with correct data
  3. Navigate directly to `/sbom/compare?left={id1}&right={id2}` and verify comparison loads automatically
  4. Verify empty state when navigating to `/sbom/compare` without query params
- Use MSW mock handlers for consistent test data across E2E tests.

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` — existing E2E test suite demonstrating Playwright patterns, page navigation, and assertion style
- `tests/setup.ts` — test setup with MSW handler registration
- `tests/mocks/handlers.ts` — existing MSW handlers for the SBOM list endpoint

## Acceptance Criteria
- [ ] E2E test: select two SBOMs from list page and navigate to comparison
- [ ] E2E test: comparison page renders all six diff sections
- [ ] E2E test: direct URL navigation with query params loads comparison
- [ ] E2E test: empty state renders when no query params are provided
- [ ] All E2E tests pass against the mock API

## Test Requirements
- [ ] Playwright E2E tests covering the four scenarios listed above
- [ ] Tests use MSW handlers for deterministic mock data

## Dependencies
- Depends on: Task 7 — Add "Compare selected" functionality to SBOM list page
