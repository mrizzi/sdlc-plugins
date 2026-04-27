# Task 4 — Frontend: Create SBOM comparison page with diff sections

## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` pointing to the new page component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (ExpandableSection + Table)
- `src/pages/SbomComparePage/components/AddedPackagesSection.tsx` — Added Packages diff section
- `src/pages/SbomComparePage/components/RemovedPackagesSection.tsx` — Removed Packages diff section
- `src/pages/SbomComparePage/components/VersionChangesSection.tsx` — Version Changes diff section
- `src/pages/SbomComparePage/components/NewVulnerabilitiesSection.tsx` — New Vulnerabilities diff section
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesSection.tsx` — Resolved Vulnerabilities diff section
- `src/pages/SbomComparePage/components/LicenseChangesSection.tsx` — License Changes diff section

## Implementation Notes
- **Page structure**: Follow the page pattern in `src/pages/SbomDetailPage/SbomDetailPage.tsx` — a page directory with a main component and a `components/` subdirectory for page-specific sub-components.
- **Route registration**: Add a lazy-loaded route in `src/routes.tsx` following the existing route definitions. The path is `/sbom/compare`.
- **URL query parameters**: Use React Router's `useSearchParams` to read `left` and `right` query params on page load. Pre-populate the SBOM selectors from these params. When the user clicks Compare, update the URL with `setSearchParams` so the comparison is bookmarkable and shareable (UC-2).
- **SBOM selectors**: Use PatternFly `Select` component (single, typeahead variant). Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: `"{name} {version}"`.
- **Compare button**: PatternFly primary `Button`, disabled until both selectors have values. On click, call `useSbomComparison` hook (from Task 3) with the selected IDs.
- **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. Export is non-MVP but include the dropdown shell (disabled state) for UI completeness; actual export logic can be implemented later.
- **Diff sections**: Each section uses PatternFly `ExpandableSection` with a title and `Badge` (count of items). Sections with >0 items are expanded by default; sections with 0 items are collapsed. Badge color varies: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- **Data tables**: Use PatternFly composable `Table` with sortable columns inside each diff section. Column definitions per section match the Figma specification (see figma-context.md for exact columns per section).
- **Virtualization**: For sections with >100 rows, use a virtualized list to prevent browser freezing per the non-functional requirement. Consider `react-window` or PatternFly's built-in virtualization.
- **New Vulnerabilities highlighting**: Rows with severity "Critical" in the New Vulnerabilities section must have a highlighted background (e.g., PatternFly danger variant row styling).
- **Severity badge**: Reuse the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in vulnerability sections.
- **Empty state**: When no comparison has been performed (no query params, initial page load), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: While comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- Per project conventions: PascalCase for components, page directory under `src/pages/`.

**Data component rendering scope:**
- All six diff section tables render data from the single `SbomComparisonResult` response — each section filters the corresponding array field (e.g., `data.added_packages` for AddedPackagesSection). This is a flat rendering scope, not per-context.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge; reuse for vulnerability sections
- `src/components/EmptyStateCard.tsx` — empty state placeholder; reference for empty state pattern
- `src/components/LoadingSpinner.tsx` — loading indicator; reference for loading pattern
- `src/components/FilterToolbar.tsx` — filter toolbar pattern; reference for toolbar layout
- `src/hooks/useSboms.ts` — existing hook to fetch SBOM list for the selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page structure pattern with sub-components directory
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table layout and column pattern
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory display pattern

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load SBOM list from existing API and support typeahead filtering
- [ ] Compare button triggers comparison API call when both SBOMs are selected
- [ ] URL updates with `left` and `right` query params when comparison is triggered
- [ ] Page loads comparison directly when accessed with `left` and `right` query params (URL-shareable)
- [ ] All six diff sections render with correct column definitions per Figma design
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Count badges display with correct colors per section type
- [ ] Critical vulnerabilities in New Vulnerabilities section have highlighted row background
- [ ] Empty state displays correctly when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] Virtualized list is used for sections with >100 rows

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors populate from SBOM list API
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: Compare button triggers API call and renders diff sections with data
- [ ] Unit test: URL query params pre-populate selectors and trigger comparison on mount
- [ ] Unit test: each diff section renders correct columns and data
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default

## Dependencies
- Depends on: Task 3 — Frontend: Add comparison API types, client function, and React Query hook
