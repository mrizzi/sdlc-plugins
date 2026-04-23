## Repository
trustify-ui

## Description
Integrate the comparison feature into the SBOM list page by adding checkbox selection and a "Compare selected" button that navigates to the comparison page. Also add MSW mock handlers, test fixtures, and an E2E test for the full comparison workflow from SBOM selection through diff rendering.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table and a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns mock comparison data
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Add tests for the new checkbox selection and compare navigation

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture with realistic data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the full comparison workflow

## Implementation Notes
- **SBOM list page changes**: In `src/pages/SbomListPage/SbomListPage.tsx`, add a checkbox column to the existing PatternFly `Table`. Track selected SBOM IDs in component state. Add a "Compare selected" `Button` to the page toolbar (following the `FilterToolbar` pattern from `src/components/FilterToolbar.tsx`). The button should be disabled unless exactly 2 SBOMs are selected. On click, use React Router's `useNavigate` to go to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}`.
- **MSW mock handler**: In `tests/mocks/handlers.ts`, add a handler matching the pattern of existing handlers for `/api/v2/sbom`. The handler should intercept `GET /api/v2/sbom/compare` and return the fixture from `tests/mocks/fixtures/sbom-comparison.json`. Ensure the handler reads `left` and `right` query params.
- **E2E test**: In `tests/e2e/sbom-compare.spec.ts`, follow the pattern in `tests/e2e/sbom-list.spec.ts`. The test should:
  1. Navigate to the SBOM list page
  2. Select two SBOMs via checkboxes
  3. Click "Compare selected"
  4. Verify navigation to `/sbom/compare` with correct query params
  5. Verify diff sections render with expected data
  6. Verify an ExpandableSection can be collapsed and expanded
- **Figma alignment**: The "Compare selected" button should use PatternFly `Button` with secondary variant, positioned in the toolbar area consistent with existing action buttons. Per Figma, the comparison navigation is the primary entry point from the SBOM list (UC-1 from the feature spec).
- **Fixture data**: The mock comparison fixture should include at least 2 entries in each diff category to enable meaningful test assertions. Include at least one critical severity vulnerability to test the highlighted row styling.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — toolbar layout pattern for placing the Compare button
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — existing fixture pattern for mock data
- `tests/e2e/sbom-list.spec.ts` — Playwright test pattern for page navigation and assertions

## Acceptance Criteria
- [ ] SBOM list page has a checkbox column for selecting SBOMs
- [ ] "Compare selected" button appears in the toolbar and is disabled unless exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] MSW mock handler returns realistic comparison data for the compare endpoint
- [ ] E2E test validates the full workflow: select SBOMs, compare, view diff sections
- [ ] Existing SBOM list page tests continue to pass

## Test Requirements
- [ ] Unit test: checkbox selection tracks selected SBOM IDs correctly
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selected SBOMs
- [ ] Unit test: "Compare selected" button is disabled with 3+ selected SBOMs
- [ ] Unit test: clicking "Compare selected" with 2 SBOMs navigates to correct URL
- [ ] E2E test: full comparison workflow from list page to comparison view renders diff sections
- [ ] E2E test: ExpandableSection can be toggled (expand/collapse)

## Dependencies
- Depends on: Task 5 — Comparison page UI
