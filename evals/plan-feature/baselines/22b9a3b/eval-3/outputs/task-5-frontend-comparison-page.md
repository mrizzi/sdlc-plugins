## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` with a header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections rendered from the comparison API response. The page supports URL-shareable comparisons by reading and writing `left` and `right` query parameters. This is the primary user-facing deliverable of the feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff section layout
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section wrapper using PatternFly `ExpandableSection` and `Badge`
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages diff category
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages diff category
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes diff category
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities diff category with critical severity row highlighting
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities diff category
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes diff category

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
Follow the page structure pattern established by `src/pages/SbomDetailPage/SbomDetailPage.tsx` with page-specific components in a `components/` subdirectory.

**Figma design specifications — Header Toolbar:**
- **Left SBOM selector**: PatternFly `Select` component (single selection, typeahead variant). Fetches the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Displays SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populated from URL query param `left`.
- **Right SBOM selector**: Identical PatternFly `Select` for the second SBOM. Pre-populated from URL query param `right`.
- **Compare button**: PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values. On click, triggers the comparison API call via `useSbomComparison` hook and updates URL query params.
- **Export dropdown**: PatternFly `Dropdown` with `variant="secondary"`. Two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. (Export is non-MVP; wire the dropdown but the download logic can be a follow-up.)

**Figma design specifications — Diff Sections:**
Each section uses a `DiffSection` wrapper component that renders a PatternFly `ExpandableSection` with:
- A title (e.g., "Added Packages")
- A PatternFly `Badge` showing the item count with section-specific color: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes
- Default expanded when the section has >0 items, collapsed when empty

Inside each section, render a PatternFly composable `Table` with sortable columns. Use virtualized rendering (e.g., `react-window` or PatternFly's built-in virtualization) for sections with >100 rows per the non-functional requirements.

**Table columns per section (from Figma):**
1. Added Packages: Package Name, Version, License, Advisories (count)
2. Removed Packages: Package Name, Version, License, Advisories (count)
3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. New Vulnerabilities: Advisory ID, Severity (render with existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" must have a highlighted background (use PatternFly's `isRowSelected` or custom `--pf-v5-global--danger-color--100` background).
5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes: Package Name, Left License, Right License

**Figma design specifications — Empty State:**
When no comparison has been performed (page loaded without query params or before clicking Compare), show a PatternFly `EmptyState` with:
- Icon: `CodeBranchIcon` from PatternFly icons
- Title: "Select two SBOMs to compare"
- Body: "Choose an SBOM for each side and click Compare to see what changed."
Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` if its interface is compatible; otherwise create inline.

**Figma design specifications — Loading State:**
While the comparison API call is in progress, render PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar controls during loading.

**URL-shareable comparisons:**
- On page load, read `left` and `right` from `useSearchParams()` (React Router v6)
- When both are present, auto-trigger the comparison
- When the user clicks Compare, update the URL query params using `setSearchParams()` so the URL is bookmarkable
- This enables UC-2 (sharing comparison URLs with compliance team)

**Route registration** — in `src/routes.tsx`, add the route for `/sbom/compare` using lazy loading, following the existing pattern for other page routes. Register the comparison route before any `/sbom/:id` dynamic route to prevent path conflicts.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing component for rendering severity levels (Critical/High/Medium/Low); use in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state component; use for the initial empty state before comparison
- `src/components/LoadingSpinner.tsx` — existing loading indicator; use as fallback while lazy-loading the page component
- `src/components/FilterToolbar.tsx` — existing filter toolbar pattern; reference for toolbar layout conventions
- `src/hooks/useSboms.ts` — existing hook to fetch SBOM list for the selectors
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page structure with sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage with package data

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Both SBOM selectors load the SBOM list and allow typeahead selection
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare calls the API and renders all six diff sections
- [ ] Each diff section shows the correct count badge with the appropriate color
- [ ] Sections with items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities section highlights rows with Critical severity
- [ ] Existing `SeverityBadge` component is used for severity rendering
- [ ] Empty state is displayed when no comparison has been performed
- [ ] Loading skeletons appear during the API call
- [ ] URL query parameters (`left`, `right`) are updated on Compare click
- [ ] Page loaded with query parameters auto-triggers the comparison
- [ ] Large diffs (>100 items in a section) use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: selectors populate with SBOM list data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: comparison data renders in correct diff sections with proper counts
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted background
- [ ] Unit test: URL params are read on mount and trigger comparison

## Dependencies
- Depends on: Task 4 — Frontend API client and hook
