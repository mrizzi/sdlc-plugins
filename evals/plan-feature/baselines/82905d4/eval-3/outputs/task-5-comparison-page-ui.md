## Repository
trustify-ui

## Description
Build the SBOM comparison page UI as specified in the Figma design context. The page includes a header toolbar with two SBOM Select dropdowns, a Compare button, and an Export Dropdown, followed by six collapsible diff sections (ExpandableSection) each containing a data Table. When no comparison is loaded, an EmptyState is shown. The page reads SBOM IDs from URL query parameters for shareable URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection with Badge count and Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM Select dropdowns, Compare button, and Export Dropdown

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to lazy-loaded `SbomComparePage`

## Implementation Notes
- **Figma component mapping**: The design specifies these PatternFly components:
  - **SBOM selectors**: Use PatternFly `Select` (single, typeahead variant) for both left and right SBOM selection. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - **Compare button**: PatternFly primary `Button`, disabled until both selectors have values. On click, update URL query params `left` and `right` which triggers the `useSbomComparison` hook.
  - **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. This is a non-MVP feature; implement the UI shell but the export logic can be a no-op placeholder.
  - **Diff sections**: Each section uses PatternFly `ExpandableSection` with a title and PatternFly `Badge` showing the item count. Badge colors per Figma: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Sections with >0 items default to expanded.
  - **Data tables**: Use PatternFly composable `Table` with sortable columns. Column definitions per section are specified in the Figma context (e.g., Added Packages: Package Name, Version, License, Advisories count).
  - **Severity indicators**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables.
  - **Empty state**: When no comparison is loaded (no query params or no data), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Follow the pattern of the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx`.
  - **Loading state**: While the API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- **URL integration**: Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. Pre-populate the Select dropdowns from URL params on page load for shareable URLs (UC-2 from the feature spec).
- **Virtualization**: For diff sections with >100 rows, implement windowed/virtualized rendering to meet the non-functional requirement of handling large diffs without browser freezing.
- **Route registration**: In `src/routes.tsx`, add the route following the existing lazy-loading pattern (e.g., `React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"))`).
- **Critical vulnerability highlighting**: In the New Vulnerabilities table, rows where `severity` is "critical" should have a highlighted/danger background color per Figma specification.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity badge for vulnerability tables
- `src/components/EmptyStateCard.tsx` — empty state pattern for initial page load
- `src/components/LoadingSpinner.tsx` — loading indicator (though Skeleton is preferred per Figma)
- `src/components/FilterToolbar.tsx` — toolbar layout pattern
- `src/hooks/useSboms.ts` — fetching SBOM list for the Select dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — pattern for rendering package data in a PatternFly Table
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — pattern for rendering advisory data

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two PatternFly Select dropdowns allow selecting SBOMs by name and version
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare updates URL query params and triggers the comparison API call
- [ ] Six collapsible diff sections render with correct titles, Badge counts, and Badge colors (green, red, blue, yellow per Figma)
- [ ] Each section contains a PatternFly Table with the correct columns as specified in Figma
- [ ] SeverityBadge is used in vulnerability tables
- [ ] Critical vulnerability rows have highlighted background
- [ ] EmptyState with CodeBranchIcon shows when no comparison is loaded
- [ ] Skeleton loading state shows during API call
- [ ] URL with `left` and `right` params pre-populates selectors and auto-triggers comparison
- [ ] Export Dropdown UI shell is present (functional export is non-MVP)

## Test Requirements
- [ ] Unit test: page renders EmptyState when no query params are present
- [ ] Unit test: Select dropdowns populate with SBOM list from useSboms hook
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: diff sections render with correct counts and Badge colors when comparison data is returned
- [ ] Unit test: critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: page reads left/right from URL search params and pre-populates selectors

## Dependencies
- Depends on: Task 4 — Frontend API layer and React Query hook
