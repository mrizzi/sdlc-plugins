## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page UI following the Figma design. The page includes a header toolbar with two SBOM selectors and a Compare button, plus six collapsible diff sections displaying the comparison results. Each diff section contains a PatternFly data table with columns matching the Figma specification. The page handles empty state (no comparison yet), loading state (comparison in progress), and error state.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
- **Figma design reference**: The comparison view uses a full-page layout with a header toolbar and vertically stacked collapsible diff sections.

- **CompareToolbar component:**
  - Two PatternFly `Select` components (single, typeahead) for SBOM selection. Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the dropdown options with SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - A primary PatternFly `Button` labeled "Compare" — disabled until both selectors have values. On click, updates the URL query params and triggers the comparison.
  - A secondary PatternFly `Dropdown` labeled "Export" with two items: "Export JSON" and "Export CSV". Disabled until comparison results are loaded.

- **DiffSection component:**
  - Wraps PatternFly `ExpandableSection` with a title and a PatternFly `Badge` showing the item count.
  - Badge color varies by section per Figma: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
  - Default expanded when count > 0, collapsed when count is 0.
  - Contains a PatternFly composable `Table` with sortable columns. For sections with >100 rows, implement virtualized scrolling to prevent browser freezing (use `react-window` or PatternFly's built-in virtualization).

- **Diff section definitions (per Figma):**
  1. **Added Packages** — columns: Package Name, Version, License, Advisories (count). Badge: green.
  2. **Removed Packages** — columns: Package Name, Version, License, Advisories (count). Badge: red.
  3. **Version Changes** — columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Badge: blue.
  4. **New Vulnerabilities** — columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Badge: red. Rows with severity "Critical" have a highlighted background (use PatternFly `isRowSelected` or custom row class).
  5. **Resolved Vulnerabilities** — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
  6. **License Changes** — columns: Package Name, Left License, Right License. Badge: yellow.

- **Empty state (per Figma):**
  - When no comparison has been performed (no query params or no results), show a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."
  - Reference the existing `EmptyStateCard` component in `src/components/EmptyStateCard.tsx` for the pattern.

- **Loading state (per Figma):**
  - While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.

- **Data component rendering scope:**
  - All six diff section tables render per-comparison data — they display results scoped to the specific left/right SBOM pair selected, not aggregated across multiple comparisons. Each table filters directly from the `SbomComparison` response fields (e.g., `data.added_packages`, `data.new_vulnerabilities`).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display; use in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state pattern; reference for the comparison empty state
- `src/components/FilterToolbar.tsx` — reusable filter toolbar pattern if filtering is needed within diff sections
- `src/components/LoadingSpinner.tsx` — existing loading indicator pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly table component patterns with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory list rendering pattern
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] Compare button is disabled until both SBOM selectors have values
- [ ] Six collapsible diff sections render with correct column layouts per Figma
- [ ] Each diff section has a count badge with the correct color
- [ ] Sections with items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Severity badges use the existing `SeverityBadge` component
- [ ] Empty state displays when no comparison is active
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] Large diff sections (>100 rows) use virtualized scrolling

## Test Requirements
- [ ] Unit test: renders empty state when no comparison is active
- [ ] Unit test: renders comparison results with all six diff sections
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: New Vulnerabilities rows with Critical severity have highlighted styling
- [ ] Unit test: sections with count > 0 are expanded by default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add useSbomComparison React Query hook

[sdlc-workflow] Description digest: sha256:cf70ff80cef79436ad5531040259cce2ed5828165eee462c67d0c6b1b41af4aa
