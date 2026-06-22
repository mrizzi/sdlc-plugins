# Task 7 — Add E2E test for SBOM comparison workflow

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a Playwright end-to-end test covering the complete SBOM comparison workflow: selecting two SBOMs from the list page, clicking "Compare selected", verifying the comparison page loads with correct diff sections, and verifying URL-based sharing by navigating directly to a comparison URL.

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/fixtures/sboms.json` — add or extend mock SBOM data to include two comparable SBOMs with known differences (if fixture data is shared with E2E tests)

## Implementation Notes
- Follow the existing E2E test pattern in `tests/e2e/sbom-list.spec.ts` for Playwright test structure, page object usage, and assertion style.
- Test setup should use MSW or equivalent API mocking to provide deterministic comparison data.
- Test scenarios should cover the two primary use cases from the feature description:
  1. UC-1: Select two SBOMs from list, click Compare, verify all diff sections render correctly
  2. UC-2: Navigate directly to a comparison URL with query params, verify the comparison loads without re-selecting SBOMs

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test showing test structure, selectors, and assertion patterns
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — MSW request handlers for API mocking
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data fixture

## Acceptance Criteria
- [ ] E2E test covers the full comparison workflow: select SBOMs -> click Compare -> verify diff sections
- [ ] E2E test covers URL-based sharing: navigate directly to comparison URL with query params -> verify comparison loads
- [ ] E2E test verifies that all six diff section types are rendered (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
- [ ] E2E test verifies that the Compare button is disabled with fewer than 2 selections
- [ ] E2E test verifies that critical vulnerability rows are visually highlighted

## Test Requirements
- [ ] E2E test: full workflow from SBOM list selection to comparison view rendering
- [ ] E2E test: direct URL navigation loads comparison without manual selection
- [ ] E2E test: empty state renders when page is loaded without query params

## Verification Commands
- `npx playwright test sbom-compare` — all comparison E2E tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add "Compare selected" action to SBOM list page
