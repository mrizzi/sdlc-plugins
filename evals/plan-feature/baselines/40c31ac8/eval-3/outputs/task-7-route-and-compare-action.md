## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route to render the new SbomComparePage, and add a "Compare selected" action to the SbomListPage so users can select two SBOMs from the list and navigate to the comparison view. This connects the new comparison UI into the existing application navigation flow.

## Files to Modify
- `src/routes.tsx` -- add route definition for `/sbom/compare` pointing to a lazy-loaded `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox selection to the SBOM table rows and a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected

## Implementation Notes
- Follow the existing route registration pattern in `src/routes.tsx` -- use `React.lazy()` for the `SbomComparePage` import to maintain lazy-loading behavior, matching how other pages are registered.
- For the SbomListPage changes: add PatternFly `Table` row selection (checkbox column) using the composable table's `select` prop. Track selected SBOM IDs in component state. Render a "Compare selected" `Button` in the toolbar (next to filters) that is disabled unless exactly 2 SBOMs are selected. On click, use React Router's `useNavigate()` to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}`.
- Follow the existing toolbar pattern in `SbomListPage.tsx` for button placement alongside `FilterToolbar`.
- Per CONVENTIONS.md §Component naming: use PascalCase for component files. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/routes.tsx` -- follow existing route definition pattern for lazy-loaded pages
- `src/pages/SbomListPage/SbomListPage.tsx` -- extend existing table with selection; follow the `FilterToolbar` integration pattern for toolbar button placement
- `src/components/FilterToolbar.tsx::FilterToolbar` -- existing toolbar component; place Compare button alongside it

## Acceptance Criteria
- [ ] Route `/sbom/compare` renders the SbomComparePage component
- [ ] SbomComparePage is lazy-loaded via `React.lazy()` in route definition
- [ ] SbomListPage table rows have selectable checkboxes
- [ ] "Compare selected" button appears in the SbomListPage toolbar
- [ ] "Compare selected" button is disabled unless exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Test: `/sbom/compare` route renders the comparison page
- [ ] Test: SbomListPage shows checkboxes on table rows
- [ ] Test: "Compare selected" button is disabled with 0 or 1 SBOMs selected
- [ ] Test: "Compare selected" button is enabled with exactly 2 SBOMs selected and navigates to correct URL

## Verification Commands
- `npx tsc --noEmit` -- no TypeScript compilation errors
- `npx vitest run src/pages/SbomListPage` -- list page tests pass with new selection behavior

## Dependencies
- Depends on: Task 2 -- Create feature branch (trustify-ui)
- Depends on: Task 6 -- Implement SBOM comparison page UI

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
