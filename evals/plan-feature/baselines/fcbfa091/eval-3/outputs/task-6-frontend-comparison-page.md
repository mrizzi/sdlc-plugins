## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with two SBOM selector dropdowns (PatternFly `Select`, single-select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly `ExpandableSection` components with count `Badge` indicators and composable `Table` components. The page reads `left` and `right` SBOM IDs from URL query parameters to support bookmarkable, shareable comparison URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component: reads left/right query params via `useSearchParams`, renders ComparisonToolbar and DiffSection components, handles empty/loading/error states
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with left/right SBOM `Select` dropdowns, primary Compare `Button`, and secondary Export `Dropdown`
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable section component wrapping PatternFly `ExpandableSection` with title, count `Badge`, and child table content
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — Composable `Table` for added/removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — Composable `Table` for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — Composable `Table` for new/resolved vulnerabilities (columns: Advisory ID, Severity via `SeverityBadge`, Title, Affected Package); rows with Critical severity get highlighted background
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — Composable `Table` for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
**Figma: Header Toolbar** — Two PatternFly `Select` components (single-select, typeahead variant) for left and right SBOM selection. Each selector displays SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate selections from URL query params `left` and `right`. Include a primary "Compare" `Button` that is disabled until both selectors have values. Include a secondary "Export" `Dropdown` with two items ("Export JSON", "Export CSV"), disabled until comparison data is loaded.

**Figma: Diff Sections** — Six PatternFly `ExpandableSection` components stacked vertically in this order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes. Each section title includes a PatternFly `Badge` showing the item count with section-specific colors: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Sections with count > 0 are default expanded; sections with count 0 are default collapsed.

**Figma: Data Tables** — Each section contains a PatternFly composable `Table` with sortable columns. Use virtualized rendering for sections with > 100 rows to prevent browser freezing (per non-functional requirements). Consider PatternFly's built-in table virtualization or `react-window`.

**Figma: New Vulnerabilities** — Rows where severity is "Critical" have a highlighted background (use PatternFly danger/warning row variant). The Severity column uses the existing `SeverityBadge` shared component from `src/components/SeverityBadge.tsx`.

**Figma: Empty State** — When no comparison has been performed (page loads without query params or before clicking Compare), render a PatternFly `EmptyState` with `CodeBranchIcon` (PatternFly fallback), title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed."

**Figma: Loading State** — While the comparison API call is in progress, show PatternFly `Skeleton` placeholders inside each diff section area. Disable the header toolbar controls during loading to prevent concurrent requests.

The SBOM selectors fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. The comparison data is fetched via the `useSbomComparison` hook created in Task 5.

URL state management: use React Router v6 `useSearchParams` to read and update `left` and `right` query params. When the user clicks Compare, update the URL params so the comparison is shareable.

Per CONVENTIONS.md §Component library: use PatternFly 5 components for all UI elements (Select, ExpandableSection, Badge, Table, EmptyState, Skeleton, Button, Dropdown).
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Naming: PascalCase for components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing severity badge component; use in VulnerabilityDiffTable for severity display
- `src/components/EmptyStateCard.tsx` — Existing empty state pattern; reference for the no-comparison empty state
- `src/components/LoadingSpinner.tsx` — Existing loading indicator; reference alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — Existing toolbar layout pattern; reference for ComparisonToolbar layout
- `src/hooks/useSboms.ts` — Existing hook for fetching SBOM list; use to populate selector dropdowns
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing page pattern with table and filters; reference for page structure
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — Existing detail page with tabs; reference for page layout
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component; reference for table column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list; reference for advisory display patterns
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping; use for critical vulnerability highlighting logic

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar containing left/right SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors are typeahead-enabled and populate from the SBOM list API via `useSboms`
- [ ] Compare button is disabled until both selectors have values
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] Page reads `left` and `right` URL query params on mount and pre-populates selectors
- [ ] Clicking Compare updates URL query params and triggers comparison API call
- [ ] URL is shareable — loading the page with `left` and `right` params directly performs the comparison
- [ ] All six diff sections render as collapsible `ExpandableSection` components in correct order
- [ ] Each section displays a count `Badge` with the correct color (green, red, blue, yellow per section)
- [ ] Sections with items > 0 are expanded by default; empty sections are collapsed
- [ ] Added Packages table shows Package Name, Version, License, Advisories columns
- [ ] Removed Packages table shows Package Name, Version, License, Advisories columns
- [ ] Version Changes table shows Package Name, Left Version, Right Version, Direction columns
- [ ] New Vulnerabilities table shows Advisory ID, Severity (SeverityBadge), Title, Affected Package columns
- [ ] Resolved Vulnerabilities table shows Advisory ID, Severity, Title, Previously Affected Package columns
- [ ] License Changes table shows Package Name, Left License, Right License columns
- [ ] Critical-severity vulnerability rows have highlighted background styling
- [ ] Empty state displays when no comparison has been performed (no query params)
- [ ] Skeleton loading placeholders display during API call; toolbar controls are disabled during loading
- [ ] Large diffs (>100 rows per section) use virtualized rendering without browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: selectors populate with SBOM list data from `useSboms`
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: clicking Compare triggers API call and renders diff sections with correct data
- [ ] Unit test: URL params pre-populate selectors and trigger comparison on mount
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: sections with zero items are collapsed by default
- [ ] Unit test: Export dropdown is disabled before comparison data loads

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Frontend API layer (useSbomComparison hook and TypeScript types must be available)
