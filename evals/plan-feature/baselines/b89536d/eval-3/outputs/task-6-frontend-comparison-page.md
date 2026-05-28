# Task 6 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection with count badge and data table
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages (same columns as added)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package); rows with "critical" severity get highlighted background
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- Follow the existing page structure pattern in `src/pages/SbomDetailPage/` — main page component in a directory with a `components/` subdirectory for page-specific components.
- **SBOM selectors**: Use PatternFly `Select` with single selection and typeahead. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version as the option label.
- **URL-shareable state**: Read `left` and `right` query parameters from the URL using React Router's `useSearchParams`. When the user clicks Compare, update the URL query params so the comparison is bookmarkable. On page load with query params, auto-trigger the comparison.
- **Compare button**: PatternFly primary `Button`, disabled until both selectors have values. On click, calls `useSbomComparison` hook from `src/hooks/useSbomComparison.ts` (Task 5).
- **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. Export is non-MVP but the dropdown should be rendered in disabled state.
- **Diff sections**: Each section uses PatternFly `ExpandableSection`. Default expanded when the section has >0 items. Each section title includes a PatternFly `Badge` with count. Badge colors: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- **Data tables**: Use PatternFly composable `Table` with sortable columns. For sections with >100 rows, implement virtualized rendering to prevent browser freezing (use `react-window` or PatternFly's built-in virtualization).
- **Severity display**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the vulnerability tables.
- **Critical vulnerability highlighting**: In the New Vulnerabilities table, apply a highlighted background CSS class to rows where `severity === "critical"`.
- **Empty state**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- **Route registration**: Add the route in `src/routes.tsx` following the existing lazy-loading pattern used for other pages (e.g., `SbomListPage`, `SbomDetailPage`). Place the `/sbom/compare` route before `/sbom/:id` to avoid route matching conflicts.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — existing page demonstrating the page structure, tab/section layout, and data loading patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing table component for packages; can serve as reference for the Added/Removed packages tables
- `src/components/SeverityBadge.tsx` — existing shared component for severity display; reuse directly in vulnerability tables
- `src/components/FilterToolbar.tsx` — existing toolbar component that may inform toolbar layout patterns
- `src/components/EmptyStateCard.tsx` — existing empty state component; use as reference for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; may complement Skeleton placeholders
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list; reuse for populating the SBOM selectors
- `src/utils/severityUtils.ts` — existing utility for severity ordering and color mapping; reuse for vulnerability table sorting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns with typeahead are displayed in the toolbar
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare triggers the comparison API call and displays results
- [ ] All six diff sections are displayed as collapsible sections with count badges
- [ ] Badge colors match the design: green (added/resolved), red (removed/new vulns), blue (version changes), yellow (license changes)
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities table highlights critical severity rows
- [ ] Existing `SeverityBadge` component is used in vulnerability tables
- [ ] URL query parameters `left` and `right` encode the selected SBOM IDs
- [ ] Loading the page with query params auto-triggers comparison
- [ ] Empty state is displayed when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] Export dropdown is visible but disabled (non-MVP)
- [ ] Large diffs (>100 changed packages) use virtualized rendering

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders comparison results when data is loaded (mock all six diff categories)
- [ ] Unit test: Compare button is disabled until both selectors have values
- [ ] Unit test: critical severity rows in New Vulnerabilities table have highlighted background
- [ ] Unit test: sections with zero items are collapsed by default
- [ ] Unit test: URL query params are updated when Compare is clicked
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/` for use by MSW handlers

## Dependencies
- Depends on: Task 5 — Add comparison API client function and React Query hook
