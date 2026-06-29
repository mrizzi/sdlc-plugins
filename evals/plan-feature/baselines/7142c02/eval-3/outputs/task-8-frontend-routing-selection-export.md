## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Wire up the SBOM comparison page to the application router, add SBOM selection checkboxes and a "Compare selected" action to the existing SBOM list page (per UC-1), add MSW mock handlers for the comparison endpoint, and add E2E tests for the comparison workflow. Also implement the export functionality (JSON/CSV) for compliance documentation.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection to the SBOM table and a "Compare selected" toolbar action that navigates to `/sbom/compare?left={id1}&right={id2}`
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare`

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow
- `src/pages/SbomComparePage/components/useExportComparison.ts` — Hook for exporting comparison data as JSON or CSV

## Implementation Notes
### Routing
- Add a lazy-loaded route in `src/routes.tsx` following the existing pattern (see `SearchPage` route as reference).
- Route path: `/sbom/compare` with the `SbomComparePage` component.

### SBOM List Page Selection (UC-1 from feature description)
- Add PatternFly checkbox selection to the SBOM table in `SbomListPage.tsx`.
- Add a toolbar action "Compare selected" (PatternFly `Button`, variant secondary) that is enabled when exactly 2 SBOMs are selected.
- Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.
- Per Figma: SBOM selectors are PatternFly `Select` (single, typeahead) showing SBOM name and version.

### Export Functionality
- Implement `useExportComparison` hook that accepts the `SbomComparison` data and provides `exportAsJson()` and `exportAsCsv()` methods.
- JSON export: download the comparison data as a formatted JSON file.
- CSV export: flatten the comparison sections into a CSV with a "Section" column indicating which diff category each row belongs to.
- Wire the Export dropdown in `CompareToolbar` (from Task 7) to call these export methods.

### MSW Mock
- Add a handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` that returns the fixture data from `tests/mocks/fixtures/sbom-comparison.json`.
- The fixture should contain representative data for all six diff sections.

- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's routing file scope.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` page component scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking. Applies: task creates `tests/e2e/sbom-compare.spec.ts` and modifies `tests/mocks/handlers.ts` matching the convention's test file scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task creates `src/pages/SbomComparePage/components/useExportComparison.ts` matching the convention's hook naming scope.
- Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/routes.tsx` — Existing route definitions pattern (lazy loading, path structure)
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing page to extend with selection functionality
- `tests/mocks/handlers.ts` — Existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` — Reference for fixture data structure
- `tests/e2e/sbom-list.spec.ts` — E2E test pattern to follow for the comparison workflow

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and lazy-loads the comparison page
- [ ] SBOM list page supports checkbox selection of SBOMs
- [ ] "Compare selected" button appears and is enabled when exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Export JSON downloads the comparison data as a `.json` file
- [ ] Export CSV downloads the comparison data as a `.csv` file with section labels
- [ ] MSW mock handler returns proper comparison fixture data
- [ ] E2E test covers the full comparison workflow: select 2 SBOMs, click Compare selected, verify comparison page renders

## Test Requirements
- [ ] Unit test: SbomListPage renders checkboxes for SBOM selection
- [ ] Unit test: "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Unit test: "Compare selected" navigates to correct URL with selected SBOM IDs
- [ ] Unit test: `useExportComparison` hook generates valid JSON output
- [ ] Unit test: `useExportComparison` hook generates valid CSV output with section labels
- [ ] E2E test: full comparison workflow from SBOM list to comparison view
- [ ] E2E test: direct navigation to `/sbom/compare?left={id1}&right={id2}` renders comparison

## Dependencies
- Depends on: Task 7 — Build SBOM comparison page UI

[sdlc-workflow] Description digest: sha256-md:27fc1d4c70ef6891aa10a1b7ffc4b684a9a03e57c42315716ec92467d182f2e2
