# Task 5 — Frontend SBOM Comparison Page with diff sections

## Repository
trustify-ui

## Description
Create the main SBOM Comparison Page at `/sbom/compare` with a header toolbar (two SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections based on the Figma design. The page reads `left` and `right` query parameters from the URL for shareable comparison links and auto-triggers the comparison when both are present. Uses virtualized lists for diff sections with more than 100 rows.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff section layout
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/AddedPackagesSection.tsx` — Collapsible section for added packages with data table
- `src/pages/SbomComparePage/components/RemovedPackagesSection.tsx` — Collapsible section for removed packages with data table
- `src/pages/SbomComparePage/components/VersionChangesSection.tsx` — Collapsible section for version changes with data table
- `src/pages/SbomComparePage/components/NewVulnerabilitiesSection.tsx` — Collapsible section for new vulnerabilities with data table and critical severity row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesSection.tsx` — Collapsible section for resolved vulnerabilities with data table
- `src/pages/SbomComparePage/components/LicenseChangesSection.tsx` — Collapsible section for license changes with data table

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **Figma design mapping** — The design specifies a full-page layout with a header toolbar and vertically stacked collapsible sections. Follow the Figma component mapping:
  - SBOM selectors: PatternFly `Select` (single, typeahead) — use the existing `useSboms` hook to populate the dropdown options
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items
  - Count badges: PatternFly `Badge` — green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes
  - Data tables: PatternFly `Table` (composable) with sortable columns
  - Severity indicator: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV"
  - Loading state: PatternFly `Skeleton` placeholders for each diff section while API call is in progress; header toolbar disabled during loading
- **URL-shareable state** — Use React Router's `useSearchParams` to read `left` and `right` query params on page load. Pre-populate the SBOM selectors from these values. When the user clicks "Compare", update the URL query params so the comparison is bookmarkable.
- **Auto-trigger** — When both `left` and `right` are present in the URL on page load, automatically trigger the comparison API call.
- **Virtualized lists** — For diff sections with more than 100 rows, use virtualization to prevent browser freezing (per non-functional requirements). Consider using `react-window` or PatternFly's built-in virtualization support.
- **Critical vulnerability highlighting** — In the New Vulnerabilities section, rows with severity "Critical" should have a highlighted/warning background color, per the Figma design.
- **Page structure** — Follow the existing page pattern in `src/pages/SbomDetailPage/` which has a main component and a `components/` subdirectory for page-specific sub-components.
- **Route registration** — Follow the lazy-loading pattern in `src/routes.tsx` consistent with existing route definitions.
- **Export functionality** — The Export dropdown should be disabled until comparison results are loaded. JSON export serializes the `SbomComparisonResult` directly. CSV export converts the diff into a flat CSV format. This is a non-MVP feature; implement a basic version that can be enhanced later.

### Data component rendering scope
- All six diff section tables render data from the single `SbomComparisonResult` response — each section displays its respective field (e.g., `AddedPackagesSection` renders `result.added_packages`). This is a flat rendering scope, not per-context or aggregated.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for rendering severity badges in the New/Resolved Vulnerabilities sections
- `src/components/FilterToolbar.tsx` — reusable filter toolbar if adding filtering to diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern (though the Figma specifies a custom empty state)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (though Figma specifies Skeleton placeholders)
- `src/hooks/useSboms.ts` — existing hook for populating SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component as a reference for table structure and column definitions
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component as a reference for rendering advisory data
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability sections

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] Left and right SBOM selectors populated from `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and updates URL query params
- [ ] All six diff sections render with correct data tables and column layouts per Figma
- [ ] Diff sections are collapsible using `ExpandableSection`, default expanded when items > 0
- [ ] Count badges show correct colors per section type
- [ ] New Vulnerabilities section highlights rows with "Critical" severity
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL with `left` and `right` params auto-triggers comparison on page load
- [ ] Virtualization activates for diff sections with > 100 rows
- [ ] Export dropdown is disabled until results are loaded

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors are populated from useSboms hook
- [ ] Unit test: Compare button is disabled when only one selector has a value
- [ ] Unit test: clicking Compare triggers useSbomComparison with correct IDs
- [ ] Unit test: diff sections render correct data from comparison result
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: New Vulnerabilities rows with Critical severity have highlighted styling
- [ ] Unit test: URL query params are read and pre-populate selectors

## Dependencies
- Depends on: Task 4 — Frontend API types, client function, and React Query hook
