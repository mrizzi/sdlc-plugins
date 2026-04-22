## Repository
trustify-ui

## Description
Enhance the SBOM list page to support selecting two SBOMs and navigating to the comparison view. Add row-level checkboxes to the SBOM table and a "Compare selected" button that becomes enabled when exactly two SBOMs are checked. Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection to the SBOM table rows, add a "Compare selected" toolbar button, and navigation logic to the comparison page

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture for MSW handlers
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` (modify existing file)

## Implementation Notes
- In `src/pages/SbomListPage/SbomListPage.tsx`, add a PatternFly composable `Table` checkbox column using the `select` composable transformer. Track selected SBOM IDs in component state with `useState<string[]>([])`.
- Add a "Compare selected" button to the existing toolbar (rendered alongside existing filter controls). Use PatternFly `Button` with `variant="secondary"`. Disable the button unless exactly 2 SBOMs are selected. On click, use React Router's `useNavigate()` to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.
- The existing `SbomListPage` already uses a PatternFly table — extend it with selection rather than replacing it. Follow the existing `FilterToolbar` pattern from `src/components/FilterToolbar.tsx` for toolbar layout.
- For the MSW mock handler in `tests/mocks/handlers.ts`, follow the existing handler patterns (e.g., the handler for `GET /api/v2/sbom`). The handler should return the fixture data from `tests/mocks/fixtures/sbom-comparison.json`.
- The mock fixture in `sbom-comparison.json` should match the `SbomComparison` response shape with sample data for each diff category.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — Toolbar layout pattern for adding the Compare button alongside existing controls
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing table to extend with selection
- `tests/mocks/handlers.ts` — Existing MSW handler patterns to follow

## Acceptance Criteria
- [ ] SBOM list table rows have checkboxes for selection
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] MSW mock handler and fixture data are available for testing

## Test Requirements
- [ ] Test that checkboxes render on SBOM list rows
- [ ] Test that "Compare selected" button is disabled with 0 or 1 selections
- [ ] Test that "Compare selected" button is enabled with exactly 2 selections
- [ ] Test that clicking "Compare selected" navigates to the correct URL

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run src/pages/SbomListPage` — SBOM list page tests pass

## Dependencies
- Depends on: Task 5 — Frontend comparison page (the target route must exist)
