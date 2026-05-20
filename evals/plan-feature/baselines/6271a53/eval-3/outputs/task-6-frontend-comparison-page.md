# Task 6 — Create SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the main SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly ExpandableSection and Table components. The page supports URL-shareable comparisons via query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component (wraps ExpandableSection + Table)
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages diff section
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages diff section
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes diff section
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities diff section
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities diff section
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes diff section

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage`

## Implementation Notes

### Page layout and state management
- Read `left` and `right` query parameters from the URL using React Router's `useSearchParams`
- Pre-populate the SBOM selectors from URL params on page load for URL-shareable comparisons
- When the user clicks Compare, update the URL query params (so the URL is bookmarkable) and trigger the `useSbomComparison` hook
- Use `useSboms` hook (existing) to populate the SBOM selector dropdowns

### Header toolbar (CompareToolbar)
- Two PatternFly `Select` components with typeahead enabled for SBOM selection
- Each selector shows SBOM name and version (e.g., "my-product-sbom v2.3.1")
- "Compare" button: PatternFly `Button` variant="primary", disabled until both selectors have values
- "Export" dropdown: PatternFly `Dropdown` with two items "Export JSON" and "Export CSV", disabled until comparison results are loaded
- Export is a non-MVP requirement — implement the dropdown UI but the actual export logic can be a no-op or TODO for now

### Diff sections
- Each section uses PatternFly `ExpandableSection` with a title and count `Badge`
- Sections default to expanded when they have >0 items, collapsed when empty
- Badge colors per section: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow
- Tables use PatternFly composable `Table` with sortable columns
- For >100 rows, use virtualized lists to prevent browser freezing (non-functional requirement)
- New Vulnerabilities table: rows with severity "Critical" get a highlighted background row style

### PatternFly component usage
- Follow the existing component patterns in `src/pages/SbomDetailPage/SbomDetailPage.tsx` and its sub-components for page structure
- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for severity display in vulnerability tables
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` during API loading state — or PatternFly `Skeleton` placeholders per the Figma spec
- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` (or PatternFly `EmptyState` directly) for the initial empty state before comparison

### Empty state
- When no comparison has been performed (no query params), show EmptyState with:
  - Icon: PatternFly `CodeBranchIcon`
  - Title: "Select two SBOMs to compare"
  - Body: "Choose an SBOM for each side and click Compare to see what changed."

### Loading state
- While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area
- Disable the header toolbar during loading

### Route registration
- Add the route in `src/routes.tsx` following the existing pattern for other pages (lazy-loaded component)
- The route path is `/sbom/compare`

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — reuse for severity display in vulnerability diff tables
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar patterns
- `src/components/EmptyStateCard.tsx` — reuse for empty state display
- `src/components/LoadingSpinner.tsx` — reuse for loading state
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — follow page structure and tab patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for package table column definitions and rendering
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory listing patterns
- `src/hooks/useSboms.ts` — reuse for populating SBOM selector dropdowns
- `src/utils/severityUtils.ts` — reuse for severity level ordering and color mapping

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selectors populated with SBOM list via typeahead
- [ ] Compare button triggers API call and displays results
- [ ] URL updates with `left` and `right` query params for shareability
- [ ] Page loads comparison directly when accessed with query params in URL
- [ ] Six diff sections render with correct data tables and column structures
- [ ] Count badges show per-section item counts with correct colors
- [ ] Sections with >0 items default to expanded; empty sections default to collapsed
- [ ] Critical vulnerability rows have highlighted background
- [ ] Empty state shown when no comparison has been performed
- [ ] Loading skeletons shown during API call
- [ ] Route registered in routes.tsx

## Test Requirements
- [ ] Unit test: page renders empty state when no query params present
- [ ] Unit test: SBOM selectors populate with SBOM list data
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: Compare button triggers comparison API call
- [ ] Unit test: diff sections render with correct data from API response
- [ ] Unit test: sections with items are expanded by default
- [ ] Unit test: critical severity rows have highlighted styling
- [ ] Unit test: URL updates with query params after comparison
- [ ] Unit test: page pre-populates selectors and triggers comparison from URL params
- [ ] Add comparison response fixture to `tests/mocks/fixtures/` for use in tests

## Dependencies
- Depends on: Task 5 — Add API types and client function for SBOM comparison
