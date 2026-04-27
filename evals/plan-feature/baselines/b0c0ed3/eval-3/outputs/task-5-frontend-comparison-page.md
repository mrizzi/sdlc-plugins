## Repository
trustify-ui

## Description
Build the SBOM comparison page UI at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with two SBOM selector dropdowns and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), and appropriate empty/loading states. This is the primary user-facing component of the SBOM comparison feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded `SbomComparePage`
- `src/App.tsx` — Verify route mounting (may not need changes if `routes.tsx` is auto-consumed)

## Implementation Notes
**PatternFly component mapping from Figma design:**
- SBOM selectors: use PatternFly `Select` component with `variant="typeahead"` for typeahead search. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: `"{name} {version}"` per Figma spec.
- Compare button: PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values.
- Export dropdown: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV"). Disabled until comparison result is loaded. Export is non-MVP but include the disabled dropdown for UI completeness.
- Diff sections: PatternFly `ExpandableSection` — each section gets a title, a PatternFly `Badge` with count, and an inner PatternFly `Table` (composable variant). Sections default to expanded when item count > 0.
- Count badge colors per Figma: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow.
- Data tables: PatternFly `Table` (composable) with sortable columns. For sections with > 100 rows, implement virtualized rendering to prevent browser freezing (use `react-window` or PatternFly's built-in virtualization).
- Severity indicator: reuse the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables.
- Empty state (no comparison performed): PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- Loading state: PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Disable the toolbar during loading.

**Table columns per Figma design:**
- Added/Removed Packages: Package Name, Version, License, Advisories (count)
- Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
- New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package. Rows with severity "Critical" must have a highlighted/warning background.
- Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
- License Changes: Package Name, Left License, Right License

**URL-shareable comparison:** Read `left` and `right` query parameters from the URL on mount. Pre-populate the SBOM selectors from these params. When the user clicks Compare, update the URL query params using React Router's `useSearchParams` so the comparison is bookmarkable and shareable.

**Route registration:** Add to `src/routes.tsx` following the existing lazy-loading pattern (e.g., `React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"))`). Place the route path at `/sbom/compare`.

**Page structure convention:** Follow the page directory structure convention from the codebase: main component file + `components/` subdirectory for page-specific components, as seen in `src/pages/SbomDetailPage/`.

**Critical vulnerability highlighting:** In the New Vulnerabilities table, rows where `severity === "critical"` must render with a PatternFly warning/danger background modifier. Use the severity utilities from `src/utils/severityUtils.ts` for severity level ordering and color mapping.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing severity badge component for vulnerability severity display; use in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — Existing empty state component; consider reusing or adapting for the comparison empty state
- `src/components/LoadingSpinner.tsx` — Existing loading indicator; may use alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — Existing reusable toolbar pattern; reference for toolbar layout conventions
- `src/hooks/useSboms.ts` — Existing hook to fetch SBOM list for populating the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component; reference for table column patterns and PatternFly Table usage
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list component; reference for advisory display patterns
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping utilities; use for critical vulnerability highlighting

## Acceptance Criteria
- [ ] `SbomComparePage` renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns with typeahead search are present, populated from the SBOM list API
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API via `useSbomComparison` and renders results
- [ ] Six diff sections render as collapsible `ExpandableSection` components with correct titles and badge colors
- [ ] Each section contains a sortable data table with the correct columns per Figma spec
- [ ] Sections with > 0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Empty state displays when no comparison has been performed (no query params)
- [ ] Loading state shows Skeleton placeholders while comparison API call is in progress
- [ ] URL query params (`left`, `right`) are updated on Compare and read on page load for shareability
- [ ] Large diffs (>100 rows per section) use virtualized list rendering

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are present
- [ ] Unit test: SbomComparePage renders comparison results when valid data is returned from the API (use MSW mock)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: DiffSection renders as expanded when item count > 0
- [ ] Unit test: DiffSection renders as collapsed when item count is 0
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: URL search params are updated when Compare is clicked

## Dependencies
- Depends on: Task 4 — Frontend API client and comparison hook (provides `useSbomComparison` hook and TypeScript interfaces)
