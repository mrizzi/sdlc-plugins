# Task 5 -- Frontend SBOM Comparison Page

## Repository
trustify-ui

## Description
Build the SbomComparePage component with a header toolbar and vertically stacked collapsible diff sections, following the Figma design specifications. The page allows users to select two SBOMs, trigger a comparison, and view structured diff results across six categories. The URL encodes both SBOM IDs for bookmark-ability and sharing.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/AddedPackagesSection.tsx` -- added packages diff table (Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesSection.tsx` -- removed packages diff table
- `src/pages/SbomComparePage/components/VersionChangesSection.tsx` -- version changes diff table (Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesSection.tsx` -- new vulnerabilities diff table (Advisory ID, Severity, Title, Affected Package) with critical row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesSection.tsx` -- resolved vulnerabilities diff table
- `src/pages/SbomComparePage/components/LicenseChangesSection.tsx` -- license changes diff table (Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` -- add route definition for `/sbom/compare` pointing to SbomComparePage with lazy loading

## Implementation Notes
- Follow the existing page structure pattern in `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` -- each page has its own directory with a main component and a `components/` subdirectory.
- Use PatternFly 5 components throughout, consistent with the rest of the application:
  - `Select` (single, typeahead) for the SBOM selectors in the header toolbar. Use the existing `useSboms` hook (`src/hooks/useSboms.ts`) to populate the options.
  - `ExpandableSection` for each diff category section. Default expanded for sections with count > 0.
  - `Badge` for count indicators with colors: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes.
  - `Table` (composable) for data display within each section with sortable columns.
  - `EmptyState` with `CodeBranchIcon` when no comparison has been performed (page load without query params). Title: "Select two SBOMs to compare". Body: "Choose an SBOM for each side and click Compare to see what changed."
  - `Skeleton` placeholder while the comparison API call is in progress.
  - `Dropdown` for the Export button with "Export JSON" and "Export CSV" options (disabled until results are loaded). Export is non-MVP but the button should be present per the Figma design.
- Use the `useSbomComparison` hook from Task 4 for data fetching.
- Read `left` and `right` SBOM IDs from URL query parameters using React Router's `useSearchParams`. Update the URL when the user selects SBOMs and clicks Compare, enabling URL-shareable comparisons.
- Reuse the existing `SeverityBadge` component (`src/components/SeverityBadge.tsx`) for severity display in the New Vulnerabilities and Resolved Vulnerabilities sections.
- Rows with severity "Critical" in the New Vulnerabilities section must have a highlighted background (use PatternFly's `isRowHighlighted` or custom CSS class).
- For large diffs (>100 changed packages in a section), use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization if available.
- Disable the header toolbar (selectors and Compare button) during the loading state.
- Add lazy loading for the route in `src/routes.tsx` following the pattern used for other pages.

**Data component rendering scope:**
- All six diff section tables render data from the single comparison API response -- each section renders its corresponding array from SbomComparisonResult (e.g., AddedPackagesSection renders `result.added_packages`). No cross-section aggregation.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- page structure pattern with table and filters
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- page with tabs/sections pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- package table component showing column patterns for package data
- `src/components/SeverityBadge.tsx` -- severity badge component to reuse in vulnerability sections
- `src/components/EmptyStateCard.tsx` -- empty state pattern to reference for the no-comparison-yet state
- `src/components/LoadingSpinner.tsx` -- loading state pattern (though Skeleton is preferred per Figma)
- `src/components/FilterToolbar.tsx` -- toolbar layout pattern to reference for the header toolbar
- `src/hooks/useSboms.ts` -- hook for populating SBOM selector dropdowns
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping for vulnerability rows

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load available SBOMs via useSboms hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and updates URL query parameters
- [ ] All six diff sections render with correct columns per the Figma design
- [ ] Sections with count > 0 are expanded by default; sections with count = 0 are collapsed
- [ ] Count badges display correct colors per section type
- [ ] Critical vulnerability rows have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Skeleton placeholders display during loading
- [ ] URL with left and right query parameters loads the comparison directly
- [ ] Export dropdown is present but disabled until results are loaded

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are provided
- [ ] Unit test: SbomComparePage renders diff sections with correct data from mock comparison response
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Critical severity rows in NewVulnerabilitiesSection have highlighted styling
- [ ] Unit test: sections with zero items are collapsed by default

## Dependencies
- Depends on: Task 4 -- Frontend API Types, Client Function, and React Query Hook
