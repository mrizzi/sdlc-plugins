## Repository
trustify-ui

## Description
Build the SBOM comparison page UI at `/sbom/compare` based on the Figma design specifications. The page includes a header toolbar with two SBOM selector dropdowns and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty and loading states, and URL-shareable comparison via query parameters. This is the primary user-facing deliverable for TC-9003.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to the new `SbomComparePage` component (lazy-loaded following existing route pattern)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and six diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section wrapper using PatternFly `ExpandableSection` with a count `Badge`; accepts title, count, badge color, and children props
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — PatternFly composable `Table` for added packages with columns: Package Name, Version, License, Advisories (count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — PatternFly composable `Table` for removed packages with columns: Package Name, Version, License, Advisories (count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — PatternFly composable `Table` for version changes with columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — PatternFly composable `Table` for new vulnerabilities with columns: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package; rows with severity "Critical" have a highlighted background
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — PatternFly composable `Table` for resolved vulnerabilities with columns: Advisory ID, Severity, Title, Previously Affected Package
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — PatternFly composable `Table` for license changes with columns: Package Name, Left License, Right License

## Implementation Notes
- **Figma header toolbar**: Use two PatternFly `Select` components (single-select, typeahead variant) for SBOM selection. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in the option label (e.g., "my-product-sbom v2.3.1"). Pre-populate selections from URL query params `left` and `right`.
- **Figma Compare button**: PatternFly primary `Button`, disabled until both selectors have values. On click, update URL query params and trigger the comparison via the `useSbomComparison` hook from `src/hooks/useSbomComparison.ts` (Task 4).
- **Figma Export dropdown**: PatternFly `Dropdown` component (secondary variant) with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. Export is a non-MVP feature; implement the dropdown UI but the export action can be a no-op stub with a TODO comment.
- **Figma diff sections**: Each section uses the `DiffSection` wrapper component which renders a PatternFly `ExpandableSection`. Sections default to expanded when they contain items (count > 0) and collapsed when empty. The count `Badge` color varies per the Figma spec: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- **Figma empty state**: When no comparison has been performed (no query params), render a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed." Reference the existing `EmptyStateCard` component in `src/components/EmptyStateCard.tsx` for the pattern.
- **Figma loading state**: While the comparison API call is in progress, render PatternFly `Skeleton` placeholders inside each diff section. Disable the header toolbar selectors and button during loading. Reference the existing `LoadingSpinner` component in `src/components/LoadingSpinner.tsx` for loading indicator patterns.
- **Figma severity display**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables. For Critical severity rows in New Vulnerabilities, apply a PatternFly danger/warning background modifier.
- **URL-shareable comparison**: Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. When the page loads with both params present, automatically trigger the comparison. This enables URL sharing (UC-2 from the feature spec).
- **Route registration**: In `src/routes.tsx`, add the `/sbom/compare` route following the existing lazy-loaded page component pattern. Place the compare route before the detail route to avoid path conflicts.
- **Virtualized lists**: For diff sections with more than 100 rows, use virtualized rendering to avoid browser freezing per the non-functional requirements. This can be deferred to a follow-up if performance testing shows it's needed, but add a TODO comment noting the requirement.

## Reuse Candidates
- `src/hooks/useSboms.ts` — React Query hook for fetching SBOM list to populate the selector dropdowns
- `src/components/SeverityBadge.tsx` — Existing shared component for rendering severity levels in vulnerability tables
- `src/components/EmptyStateCard.tsx` — Existing empty state component pattern to follow for the initial empty state
- `src/components/LoadingSpinner.tsx` — Loading indicator pattern reference
- `src/components/FilterToolbar.tsx` — PatternFly toolbar layout pattern reference for the header toolbar
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component as a pattern reference for the package-related diff tables
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list component as a pattern reference for the vulnerability tables
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping utilities for vulnerability display

## Acceptance Criteria
- [ ] `/sbom/compare` route renders the comparison page
- [ ] Both SBOM selector dropdowns load and display available SBOMs via the `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare updates the URL query params and triggers the comparison API call
- [ ] All six diff sections render with correct data, column structure, and badge colors per the Figma spec
- [ ] New Vulnerabilities table rows with "Critical" severity have highlighted backgrounds
- [ ] Empty state displays when no comparison has been performed (no URL params)
- [ ] Loading skeletons display while the API call is in progress
- [ ] URL with `left` and `right` query params auto-triggers comparison on page load (URL-shareable)
- [ ] Export dropdown renders with JSON and CSV options (stub implementation acceptable for non-MVP)

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors populate with options from the `useSboms` hook
- [ ] Unit test: Compare button is disabled when only one selector has a value
- [ ] Unit test: clicking Compare triggers the `useSbomComparison` hook with selected IDs
- [ ] Unit test: diff sections render with correct data and counts when comparison data is loaded
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: loading state shows skeletons while comparison is in progress

## Dependencies
- Depends on: Task 4 — Frontend API and hook for SBOM comparison
