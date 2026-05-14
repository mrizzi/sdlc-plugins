# Task 5 — Add SBOM selection on list page and comparison navigation

## Repository
trustify-ui

## Target Branch
main

## Description
Add checkbox-based multi-selection to the SBOM list page so users can select two SBOMs and navigate to the comparison view. This implements the primary entry point for the comparison workflow (UC-1): user selects two SBOMs on the list page, clicks "Compare selected", and is navigated to `/sbom/compare?left={id1}&right={id2}`. The "Compare selected" button is disabled unless exactly two SBOMs are checked.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and a "Compare selected" toolbar action button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Add tests for the selection and comparison navigation behavior

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data for MSW handlers
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the full comparison workflow (select SBOMs, navigate, verify comparison page)

## Implementation Notes
- **Checkbox selection**: Add a checkbox column as the first column of the SBOM table in `SbomListPage.tsx`. Use PatternFly's composable `Table` select pattern — add `Td` with `select` prop for each row. Track selected SBOM IDs in component state using `useState<string[]>`.
- **Compare action button**: Add a "Compare selected" `Button` to the page toolbar (next to existing filter controls). Disable the button unless `selectedIds.length === 2`. On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`.
- **Selection limit**: Optionally show an inline alert or tooltip when a user tries to select more than 2 SBOMs, informing them that exactly two are needed for comparison.
- Follow the existing toolbar pattern in `SbomListPage.tsx` — add the Compare button alongside the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx`.
- **MSW mock handler**: Add a handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` that returns the mock fixture data from `tests/mocks/fixtures/sbom-comparison.json`.
- **E2E test**: Follow the pattern in `tests/e2e/sbom-list.spec.ts` for Playwright test structure. The E2E test should: load the SBOM list page, select two SBOMs, click "Compare selected", verify navigation to the comparison page, and verify diff sections render.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page to extend with selection functionality
- `src/components/FilterToolbar.tsx` — existing toolbar component pattern for adding the Compare button
- `tests/mocks/handlers.ts` — existing MSW handlers to extend with comparison endpoint mock
- `tests/mocks/fixtures/sboms.json` — existing mock fixture pattern to follow for `sbom-comparison.json`
- `tests/e2e/sbom-list.spec.ts` — existing E2E test pattern to follow for the comparison E2E test

## Acceptance Criteria
- [ ] SBOM list page table includes a checkbox column for row selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" with 2 SBOMs selected navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] MSW mock handler for the comparison endpoint exists in test setup
- [ ] E2E test covers the full comparison workflow from SBOM list to comparison page

## Test Requirements
- [ ] Unit test: checkbox selection adds/removes SBOM IDs from selection state
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with left and right params
- [ ] E2E test: full workflow — select two SBOMs, click Compare, verify comparison page renders with diff sections

## Dependencies
- Depends on: Task 4 — Add SBOM comparison page with Figma-specified UI
