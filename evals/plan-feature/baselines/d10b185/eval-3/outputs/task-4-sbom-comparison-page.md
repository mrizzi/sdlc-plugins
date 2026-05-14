# Task 4 — Add SBOM comparison page with Figma-specified UI

## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown, followed by vertically stacked collapsible diff sections. Each diff section uses PatternFly `ExpandableSection` with a count `Badge` and a data `Table` inside. The page handles empty state (no comparison yet), loading state (API call in progress), and result state (comparison data rendered). This is the primary user-facing deliverable of the SBOM comparison feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **Page structure**: Follow the page directory convention in `src/pages/` — each page gets its own directory with a main component, test file, and `components/` subdirectory. See `src/pages/SbomDetailPage/` for reference.

- **Figma component mapping** (PatternFly 5 components):
  - SBOM selectors: PatternFly `Select` (single, typeahead variant). Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option.
  - Compare button: PatternFly `Button` (primary variant). Disabled until both selectors have values. On click, sets URL query params `left` and `right` and triggers the `useSbomComparison` hook.
  - Export dropdown: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV"). Disabled until comparison data is loaded.
  - Diff sections: PatternFly `ExpandableSection` with `isExpanded` defaulting to `true` for sections with >0 items. Each section title includes a PatternFly `Badge` showing the item count.
  - Data tables: PatternFly composable `Table` (`Thead`, `Tbody`, `Tr`, `Th`, `Td`). Sortable columns. For sections with >100 rows, implement virtualized rendering to prevent browser freezing (per non-functional requirements).
  - Severity indicator: Use existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities sections.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Disable the header toolbar during loading.

- **Diff section details** (per Figma specifications):
  1. **Added Packages** — Badge color: green. Columns: Package Name, Version, License, Advisories (count).
  2. **Removed Packages** — Badge color: red. Columns: Package Name, Version, License, Advisories (count).
  3. **Version Changes** — Badge color: blue. Columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
  4. **New Vulnerabilities** — Badge color: red. Columns: Advisory ID, Severity (SeverityBadge), Title, Affected Package. Rows with severity "Critical" get highlighted background.
  5. **Resolved Vulnerabilities** — Badge color: green. Columns: Advisory ID, Severity, Title, Previously Affected Package.
  6. **License Changes** — Badge color: yellow. Columns: Package Name, Left License, Right License.

- **URL-shareable comparison**: Read `left` and `right` query params from the URL on mount. If both are present, auto-populate the selectors and trigger the comparison. When the user clicks Compare, update the URL query params using React Router's `useSearchParams` so the comparison is bookmarkable and shareable.

- **Data component rendering scope**: All six diff section tables render data from the single `SbomComparison` response. Each table filters to its specific category (e.g., `comparison.added_packages` for the Added Packages table). These are all top-level data — no per-context filtering within nested containers.

- **Export functionality**: The Export dropdown generates a JSON or CSV file from the current comparison data client-side. Use `Blob` and `URL.createObjectURL` for download. This is a non-MVP feature but included in the UI per the Figma design.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability sections
- `src/components/EmptyStateCard.tsx` — existing empty state component (may need adaptation for the comparison-specific empty state)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (Skeleton is preferred per Figma, but this shows the project's loading pattern)
- `src/components/FilterToolbar.tsx` — reusable toolbar component pattern for reference
- `src/hooks/useSboms.ts` — existing hook to populate SBOM selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page structure with sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage pattern

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load and display available SBOMs using `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and renders results in the six diff sections
- [ ] Each diff section is a PatternFly `ExpandableSection` with a count `Badge` in the correct color
- [ ] Sections with >0 items default to expanded; sections with 0 items default to collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows `Skeleton` placeholders during API call
- [ ] URL query params `left` and `right` are updated when Compare is clicked
- [ ] Opening the page with both query params pre-populated auto-triggers comparison
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] Page handles large diffs (>100 rows per section) with virtualized rendering

## Test Requirements
- [ ] Unit test: empty state renders when no query params are present
- [ ] Unit test: SBOM selectors populate with SBOM list data
- [ ] Unit test: Compare button is disabled when only one selector has a value
- [ ] Unit test: clicking Compare triggers the comparison hook and renders diff sections
- [ ] Unit test: each diff section renders the correct columns and data
- [ ] Unit test: critical vulnerability rows receive highlighted styling
- [ ] Unit test: loading state shows Skeleton placeholders
- [ ] Unit test: URL query params are read on mount and auto-trigger comparison

## Dependencies
- Depends on: Task 3 — Add comparison API client, TypeScript types, and React Query hook
