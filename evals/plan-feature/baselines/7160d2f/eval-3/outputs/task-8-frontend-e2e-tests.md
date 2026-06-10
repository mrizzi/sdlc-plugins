## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add end-to-end tests for the SBOM comparison workflow covering the full user journey: selecting two SBOMs from the list page, navigating to the comparison view, verifying diff sections render correctly, and testing URL shareability.

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the SBOM comparison workflow

## Implementation Notes
Follow the existing E2E test pattern in `tests/e2e/sbom-list.spec.ts` for test structure, page navigation, and assertion patterns.

Test scenarios to cover:
1. **Full comparison workflow (UC-1)**: Navigate to SBOM list page, select two SBOMs via checkboxes, click "Compare selected", verify comparison page loads with diff sections.
2. **URL shareability (UC-2)**: Navigate directly to `/sbom/compare?left={id1}&right={id2}`, verify selectors are pre-populated and comparison results render.
3. **Empty state**: Navigate to `/sbom/compare` without query params, verify empty state message "Select two SBOMs to compare" is displayed.
4. **Diff section content**: Verify that each diff section (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) displays correct data.
5. **Critical vulnerability highlighting**: Verify that rows with Critical severity in New Vulnerabilities have visual emphasis.

Use the existing test setup from `tests/setup.ts` and MSW handlers from `tests/mocks/handlers.ts`.

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test demonstrating the project's E2E test patterns and page object usage
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — MSW request handlers (will need comparison endpoint handler from Task 5)

## Acceptance Criteria
- [ ] E2E test covers the full comparison workflow from SBOM list selection to diff rendering
- [ ] E2E test covers direct URL navigation with pre-populated selectors
- [ ] E2E test verifies empty state when no comparison is active
- [ ] All E2E tests pass in CI

## Test Requirements
- [ ] Playwright E2E test for UC-1: select two SBOMs, compare, verify diff sections
- [ ] Playwright E2E test for UC-2: navigate via URL with query params, verify pre-populated state
- [ ] Playwright E2E test for empty state display
- [ ] Playwright E2E test for Critical vulnerability row highlighting

## Verification Commands
- `npx playwright test sbom-compare` — run the SBOM comparison E2E tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 7 — Add SBOM selection UI to SbomListPage
