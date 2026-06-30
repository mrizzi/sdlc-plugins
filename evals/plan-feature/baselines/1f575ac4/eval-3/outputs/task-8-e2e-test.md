## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a Playwright end-to-end test covering the full SBOM comparison workflow: selecting two SBOMs from the list page, navigating to the comparison view, verifying the diff sections render correctly, and testing URL sharing by loading a comparison URL directly.

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Implementation Notes
- Follow the existing E2E test pattern in `tests/e2e/sbom-list.spec.ts` for test structure, page navigation, and assertion patterns.
- Test scenarios:
  1. Navigate to SBOM list, select two SBOMs via checkboxes, click "Compare selected", verify comparison page loads with diff sections
  2. Load `/sbom/compare?left={id1}&right={id2}` directly and verify comparison auto-triggers and diff sections render
  3. Verify empty state displays when navigating to `/sbom/compare` without query params
- Use existing MSW handlers and fixtures for API mocking (or Playwright's route interception if the E2E setup uses real browser requests).

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` — existing E2E test; follow its patterns for page navigation and assertions
- `tests/setup.ts` — test setup configuration
- `tests/mocks/handlers.ts` — MSW handlers; extend with comparison endpoint mock if E2E uses MSW

## Acceptance Criteria
- [ ] E2E test covers the full comparison workflow from SBOM list to comparison view
- [ ] E2E test covers direct URL loading of a comparison
- [ ] E2E test covers empty state
- [ ] All E2E tests pass

## Test Requirements
- [ ] Playwright E2E test for select-and-compare workflow
- [ ] Playwright E2E test for direct URL comparison loading
- [ ] Playwright E2E test for empty state display

## Verification Commands
- `npx playwright test sbom-compare` — run the comparison E2E tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 6 — Frontend comparison page
- Depends on: Task 7 — SBOM list page compare action
