# Task 5 — SBOM comparison page with diff sections UI

## Repository
trustify-ui

## Description
Create the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page reads SBOM IDs from URL query parameters to support shareable comparison URLs.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the new page component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section with count badge and data table
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — table for added packages section
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — table for removed packages section
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — table for version changes section
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — table for new vulnerabilities section
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — table for resolved vulnerabilities section
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — table for license changes section

## Implementation Notes
- **Figma design reference**: the comparison view uses these PatternFly components:
  - `Select` (single, typeahead) for SBOM selectors — fetches the SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`
  - `ExpandableSection` for each diff section — default expanded for sections with >0 items
  - `Badge` for count badges — color varies by section: green for Added/Resolved, red for Removed/New Vulnerabilities, blue for Version Changes, yellow for License Changes
  - `Table` (composable) for data tables within each section — sortable columns
  - `EmptyState` for the initial state when no comparison is loaded — use `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - `Skeleton` for loading state placeholders during API call
  - `Dropdown` for the Export button with "Export JSON" and "Export CSV" options (export is non-MVP but the button should be present and disabled or show a "Coming soon" tooltip)
- **URL-shareable comparisons**: read `left` and `right` from URL search params using React Router's `useSearchParams`. When both are present, auto-trigger the comparison on page load. When the user clicks Compare, update the URL search params using `setSearchParams` to make the comparison bookmarkable.
- **Page structure** follows the existing page pattern: each page has its own directory under `src/pages/` with a main component and a `components/` subdirectory. Reference `src/pages/SbomDetailPage/SbomDetailPage.tsx` for the directory and component organization pattern.
- **Route registration**: add a lazy-loaded route in `src/routes.tsx` following the pattern of existing routes. The route path should be `/sbom/compare`. Register this route BEFORE the `/sbom/:id` route to prevent the router from matching "compare" as an ID parameter.
- **Data table columns per section** (from Figma):
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package — rows with severity "Critical" must have a highlighted/warning background
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Virtualization**: for sections with >100 rows, implement virtualized list rendering to prevent browser freezing. Use `react-window` or a similar virtualization library. This is a non-functional requirement from the feature spec.
- **SeverityBadge**: reuse the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in vulnerability tables.
- **Critical vulnerability highlighting**: in the New Vulnerabilities table, rows where `severity === "critical"` should have a PatternFly warning/danger background color applied via a custom row class.

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see Task 4 for full type definition; defined in `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- `GET /api/v2/sbom` — existing endpoint returning paginated SBOM list for selector dropdowns (see `modules/fundamental/src/sbom/endpoints/list.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing hook for fetching the SBOM list; reuse for the SBOM selector dropdowns
- `src/components/SeverityBadge.tsx` — existing severity badge component; reuse in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state component; reference for the empty state pattern (may need a more specific empty state for this page)
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reference for loading state pattern
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for toolbar layout pattern
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — existing page component demonstrating page directory structure and tab/section layout
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table column definition and rendering pattern
- `src/utils/severityUtils.ts` — existing severity ordering and color mapping utilities; reuse for critical vulnerability highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns allow searching and selecting SBOMs
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the API call and renders six collapsible diff sections
- [ ] Each section shows a count badge with the correct color per Figma spec
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Data tables display the correct columns per section as defined in Figma
- [ ] New Vulnerabilities rows with "critical" severity have a highlighted background
- [ ] Existing SeverityBadge component is used for severity display
- [ ] Empty state renders when no comparison has been performed (no URL params)
- [ ] Loading state shows Skeleton placeholders while the API call is in progress
- [ ] URL encodes both SBOM IDs as query parameters for bookmarkable URLs
- [ ] Page auto-triggers comparison when loaded with both `left` and `right` URL params
- [ ] Export dropdown is present (can be disabled/placeholder for non-MVP)
- [ ] Sections with >100 rows use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOM IDs are in URL
- [ ] Unit test: page renders comparison results when API returns data (use MSW mock)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: URL params are updated when Compare is clicked

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation passes
- `npx vitest run --reporter=verbose` — unit tests pass

## Dependencies
- Depends on: Task 4 — API types, client function, and React Query hook
