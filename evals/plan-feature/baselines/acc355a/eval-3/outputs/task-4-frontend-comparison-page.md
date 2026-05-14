# Task 4 — Add SBOM comparison page with diff section components

## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly `Select` with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly `ExpandableSection` and `Table` components. The page supports URL-shareable comparisons by reading `left` and `right` query parameters from the URL.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff section layout
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and `Table`
- `src/pages/SbomComparePage/components/AddedPackagesSection.tsx` — Added packages diff section (columns: Package Name, Version, License, Advisories count; green badge)
- `src/pages/SbomComparePage/components/RemovedPackagesSection.tsx` — Removed packages diff section (columns: Package Name, Version, License, Advisories count; red badge)
- `src/pages/SbomComparePage/components/VersionChangesSection.tsx` — Version changes diff section (columns: Package Name, Left Version, Right Version, Direction; blue badge)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesSection.tsx` — New vulnerabilities diff section (columns: Advisory ID, Severity via `SeverityBadge`, Title, Affected Package; red badge; critical rows highlighted)
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesSection.tsx` — Resolved vulnerabilities diff section (columns: Advisory ID, Severity, Title, Previously Affected Package; green badge)
- `src/pages/SbomComparePage/components/LicenseChangesSection.tsx` — License changes diff section (columns: Package Name, Left License, Right License; yellow badge)

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **Figma component mapping**: Follow the component mapping from the Figma design context:
  - SBOM selectors: PatternFly `Select` (single, typeahead variant). Use the existing `useSboms` hook (`src/hooks/useSboms.ts`) to populate the dropdown options with SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - Diff sections: PatternFly `ExpandableSection`. Default expanded for sections with >0 items. Each section title includes a PatternFly `Badge` with the item count.
  - Data tables: PatternFly `Table` (composable). Sortable columns.
  - Severity indicator: Use existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while loading. Disable the header toolbar during loading.
  - Export button: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded.
- **Badge colors per section**: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow.
- **Critical vulnerability highlighting**: In the New Vulnerabilities section, rows where severity is "Critical" must have a highlighted/warning background (use PatternFly row variant or custom class).
- **URL-shareable comparison**: Read `left` and `right` from URL search params on mount. If both are present, pre-populate the selectors and trigger comparison automatically. When the user clicks Compare, update the URL search params using `useSearchParams` from React Router.
- **Virtualized lists**: For diff sections with >100 items, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization.
- **Page structure convention**: Follow the existing page directory pattern under `src/pages/` — each page gets its own directory with a main component and a `components/` subdirectory for page-specific components.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — reuse for severity display in vulnerability sections
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern (though the comparison page uses a custom empty state per Figma)
- `src/components/LoadingSpinner.tsx` — reference for loading state pattern
- `src/components/FilterToolbar.tsx` — reference for toolbar layout patterns with PatternFly
- `src/hooks/useSboms.ts` — reuse to populate SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory data display patterns
- `src/utils/severityUtils.ts` — reuse severity ordering and color mapping for vulnerability sections

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and lazy-loads `SbomComparePage`
- [ ] Header toolbar displays two SBOM selector dropdowns with typeahead search populated from `useSboms`
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls `useSbomComparison` with the selected SBOM IDs and updates URL search params
- [ ] Six diff sections render with correct columns, count badges, and badge colors per Figma design
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Empty state displays when no comparison has been performed (no query params)
- [ ] Loading state shows Skeleton placeholders and disables toolbar during API call
- [ ] New Vulnerabilities section highlights rows with Critical severity
- [ ] URL with `left` and `right` query params auto-triggers comparison on page load
- [ ] Export dropdown is present and disabled until comparison result is loaded

## Test Requirements
- [ ] Unit test: empty state renders when no query params are present
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button triggers API call when both SBOMs are selected
- [ ] Unit test: diff sections render with correct data from mock comparison response
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: URL query params pre-populate selectors and auto-trigger comparison

## Dependencies
- Depends on: Task 3 — Add API types, client function, and React Query hook for SBOM comparison
