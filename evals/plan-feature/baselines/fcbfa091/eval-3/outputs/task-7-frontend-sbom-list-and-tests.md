## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Update the SBOM list page to support selecting two SBOMs for comparison, and add test infrastructure for the comparison feature. This task adds checkbox selection to the SBOM list table, a "Compare selected" toolbar action that navigates to the comparison page, MSW mock handlers/fixtures for the comparison API, and unit tests for the comparison page components.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page covering empty state, selector behavior, Compare button state, diff section rendering, URL param handling, and critical vulnerability highlighting
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture data
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test: select two SBOMs from list, click Compare, verify comparison page renders with diff sections

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to SBOM table for multi-select; add "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected; button is disabled unless exactly two SBOMs are checked
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` returning mock comparison data from the fixture

## Implementation Notes
For the SBOM list page changes, add a PatternFly checkbox column to the existing table in `src/pages/SbomListPage/SbomListPage.tsx`. Track selected SBOM IDs in local component state. Add a "Compare selected" button to the toolbar (follow the existing `FilterToolbar` pattern from `src/components/FilterToolbar.tsx`) that:
1. Is disabled when the number of selected SBOMs is not exactly 2
2. On click, navigates to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router `useNavigate`

For MSW mocks, follow the existing pattern in `tests/mocks/handlers.ts` — add a handler for `GET /api/v2/sbom/compare` that returns the fixture from `tests/mocks/fixtures/sbom-comparison.json`. The fixture should contain representative data for all six diff categories.

For unit tests, follow the existing pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` — use React Testing Library with MSW for API mocking.

For the E2E test, follow the pattern in `tests/e2e/sbom-list.spec.ts` — navigate to the SBOM list, select two SBOMs, click Compare, and verify the comparison page renders with diff sections.

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Component library: use PatternFly 5 components for all UI elements.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing SBOM list page; modify to add checkbox selection
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Existing test pattern; reference for test setup and MSW usage
- `src/components/FilterToolbar.tsx` — Existing toolbar pattern; reference for placing the Compare button
- `tests/mocks/handlers.ts` — Existing MSW handlers; follow pattern for adding comparison endpoint mock
- `tests/mocks/fixtures/sboms.json` — Existing fixture pattern; reference for comparison fixture structure
- `tests/e2e/sbom-list.spec.ts` — Existing E2E test; reference for Playwright navigation and assertion patterns
- `tests/setup.ts` — Test setup with MSW and render helpers; reference for test configuration

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for multi-select
- [ ] "Compare selected" button appears in the SBOM list toolbar
- [ ] "Compare selected" button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking "Compare selected" with two SBOMs navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] MSW mock handler for comparison endpoint returns valid fixture data
- [ ] Unit tests cover comparison page empty state, selector behavior, Compare button state, diff section rendering, and URL param handling
- [ ] E2E test verifies the full comparison workflow from SBOM list to comparison page

## Test Requirements
- [ ] Unit test: SbomListPage renders checkbox column in SBOM table
- [ ] Unit test: "Compare selected" button is disabled when 0 or 1 SBOMs are selected
- [ ] Unit test: "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to correct comparison URL
- [ ] Unit test: SbomComparePage renders empty state when no query params
- [ ] Unit test: SbomComparePage renders comparison results with all six diff sections
- [ ] Unit test: critical vulnerability rows are highlighted
- [ ] E2E test: select two SBOMs from list, click Compare, verify comparison page renders with diff data

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Frontend comparison page (the comparison page must exist to test and navigate to)
