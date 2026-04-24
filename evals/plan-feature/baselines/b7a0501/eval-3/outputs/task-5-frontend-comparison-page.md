## Repository
trustify-ui

## Description
Build the SBOM comparison page UI at `/sbom/compare` based on the Figma design specifications. The page includes a header toolbar with two SBOM selectors and a compare button, six collapsible diff sections with data tables, an export dropdown, empty state, and loading state. This is the primary user-facing component for the SBOM comparison feature (TC-9003).

## Files to Modify
- `src/routes.tsx` — Add route `/sbom/compare` pointing to `SbomComparePage` with lazy loading

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, compare button, export dropdown), diff section rendering, empty state, and loading state
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section using PatternFly `ExpandableSection` with count `Badge` and configurable badge color
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package) with critical row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes (columns: Package Name, Left License, Right License)

## Implementation Notes
- **Page structure**: Follow the existing page directory pattern in `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` — a main page component with a `components/` subdirectory for page-specific sub-components.
- **SBOM selectors**: Use PatternFly `Select` (single, typeahead) for both left and right SBOM selectors. Populate the dropdown options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in the selector labels (e.g., "my-product-sbom v2.3.1").
- **URL state**: Pre-populate selectors from URL query params `left` and `right`. When the user clicks "Compare", update the URL with the selected SBOM IDs using React Router's `useSearchParams` — this makes comparisons URL-shareable per UC-2.
- **Compare button**: Primary PatternFly button, disabled until both selectors have values. On click, trigger the comparison by updating URL params (which triggers the `useSbomComparison` hook from Task 4).
- **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded. This is a non-MVP feature per the requirements — implement the UI shell but the actual export logic can be a no-op placeholder.
- **Diff sections**: Each section uses the `DiffSection` wrapper component with PatternFly `ExpandableSection`. Sections appear in order: Added Packages (green badge), Removed Packages (red badge), Version Changes (blue badge), New Vulnerabilities (red badge), Resolved Vulnerabilities (green badge), License Changes (yellow badge). Sections with >0 items are expanded by default; empty sections are collapsed by default.
- **Data tables**: Use PatternFly composable `Table` with sortable columns. For the New Vulnerabilities table, rows with `severity === "critical"` must have a highlighted background (use PatternFly's `isRowHighlighted` or a custom row class).
- **Severity display**: Use the existing `SeverityBadge` shared component from `src/components/SeverityBadge.tsx` for severity columns in the vulnerability tables.
- **Empty state**: When no comparison has been performed (no query params on initial load), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` if it accepts custom icon/title/body props; otherwise create a minimal inline empty state.
- **Loading state**: While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the header toolbar during loading.
- **Virtualization**: For diff sections with more than 100 rows, use virtualized rendering to prevent browser freezing per the non-functional requirements.
- **Route registration**: Add the route in `src/routes.tsx` using lazy loading (`React.lazy`) consistent with existing page routes. The route path should be `/sbom/compare` and must be registered before `/sbom/:id` to avoid path conflicts.

## Reuse Candidates
- `src/hooks/useSboms.ts` — Existing hook to fetch SBOM list for selector dropdowns
- `src/components/SeverityBadge.tsx` — Existing shared component for severity display in vulnerability tables
- `src/components/EmptyStateCard.tsx` — Existing empty state component (check if reusable with custom props)
- `src/components/FilterToolbar.tsx` — Reference for PatternFly toolbar layout patterns
- `src/components/LoadingSpinner.tsx` — Existing loading indicator (for fallback loading state)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Reference for PatternFly table implementation with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Reference for advisory data display patterns
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping for vulnerability tables
- `src/utils/formatDate.ts` — Date formatting if any date columns are displayed

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with the header toolbar and empty state on initial load
- [ ] Left and right SBOM selectors are populated with SBOM options from the API
- [ ] Selecting two SBOMs and clicking "Compare" updates the URL and triggers the comparison API call
- [ ] All six diff sections render with correct data tables and column layouts per the Figma design
- [ ] Diff sections use correct badge colors: green (added/resolved), red (removed/new vulns), blue (version changes), yellow (license changes)
- [ ] Sections with items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities table highlights rows with critical severity
- [ ] Severity badges use the existing `SeverityBadge` component
- [ ] Loading state shows skeleton placeholders and disables the toolbar
- [ ] Empty state shows the correct icon, title, and body text
- [ ] URL with `left` and `right` query params loads the comparison directly (UC-2: shareable URL)
- [ ] Export dropdown renders with JSON and CSV options (UI only for MVP)

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors display options from the `useSboms` hook
- [ ] Unit test: clicking "Compare" updates URL search params with selected SBOM IDs
- [ ] Unit test: diff sections render with correct data when comparison data is provided
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: loading state shows skeletons and disables toolbar
- [ ] Unit test: URL query params pre-populate the SBOM selectors and trigger comparison

## Dependencies
- Depends on: Task 4 — Frontend API layer and hook
