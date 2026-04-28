# Task 4 — Frontend: SBOM comparison page UI and routing

## Repository
trustify-ui

## Description
Create the SBOM comparison page at `/sbom/compare` with a header toolbar containing two SBOM selectors (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, render six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) using PatternFly ExpandableSection components with data tables inside. Support URL-shareable comparisons by reading `left` and `right` query parameters from the URL.

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` pointing to the new page component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — page-level tests
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section wrapper
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table for added/removed packages
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — table for version changes
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table for new/resolved vulnerabilities
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table for license changes

## Implementation Notes

### Page layout (from Figma design)

The page is a full-page layout following existing page patterns (see `src/pages/SbomDetailPage/SbomDetailPage.tsx`).

**Header toolbar:**
- Two PatternFly `Select` components (single-select, typeahead) for choosing left and right SBOMs
- Pre-populate selections from URL query params `left` and `right` using `useSearchParams()` from React Router
- Fetch SBOM list for selectors using the existing `useSboms` hook from `src/hooks/useSboms.ts`
- Display SBOM name and version in selector options (e.g., "my-product-sbom v2.3.1")
- "Compare" button (PatternFly `Button`, variant `primary`): disabled until both selectors have values; on click, update URL query params and trigger the comparison via `useSbomComparison` hook
- "Export" dropdown (PatternFly `Dropdown`): two items — "Export JSON" and "Export CSV"; disabled until comparison data is loaded

**URL-shareable comparisons:**
- When the page loads with `?left={id1}&right={id2}` in the URL, auto-populate selectors and trigger comparison immediately
- When the user clicks Compare, update the URL query params using `useSearchParams` setter so the URL is always bookmarkable
- This satisfies the "URL-shareable comparison" requirement (UC-2)

### Diff sections (from Figma design)

Each section uses the `DiffSection` wrapper component which wraps PatternFly `ExpandableSection`:
- Title with section name
- Count `Badge` showing number of items (color per Figma: green for added/resolved, red for removed/new vulns, blue for version changes, yellow for license changes)
- Default expanded when count > 0, collapsed when count is 0

**Section order and table columns (per Figma):**

1. **Added Packages** — `PackageDiffTable`: Package Name, Version, License, Advisories (count). Badge: green.
2. **Removed Packages** — `PackageDiffTable`: Package Name, Version, License, Advisories (count). Badge: red.
3. **Version Changes** — `VersionChangeTable`: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Badge: blue.
4. **New Vulnerabilities** — `VulnerabilityDiffTable`: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Badge: red. Rows with severity "critical" must have a highlighted/warning background.
5. **Resolved Vulnerabilities** — `VulnerabilityDiffTable`: Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
6. **License Changes** — `LicenseChangeTable`: Package Name, Left License, Right License. Badge: yellow.

All tables use PatternFly composable `Table` with sortable columns.

### Virtualized lists for large diffs

Per non-functional requirements, use virtualized lists when a diff section has more than 100 items to prevent browser freezing. Use a virtualization library compatible with PatternFly tables (e.g., `react-window` or PatternFly's built-in virtualization).

### Empty state

When no comparison has been performed (no query params, page first load), display PatternFly `EmptyState` with:
- Icon: `CodeBranchIcon` from PatternFly icons
- Title: "Select two SBOMs to compare"
- Body: "Choose an SBOM for each side and click Compare to see what changed."

Follow the existing empty state pattern in `src/components/EmptyStateCard.tsx`.

### Loading state

While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.

### Route registration

In `src/routes.tsx`, add the `/sbom/compare` route. Use lazy loading for the page component following the existing pattern. Ensure the route is registered before `/sbom/:id` if a wildcard SBOM detail route exists, to avoid path conflicts.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page layout structure, tab/section organization
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for table component pattern with PatternFly Table
- `src/components/SeverityBadge.tsx` — existing component for rendering severity levels in vulnerability tables
- `src/components/EmptyStateCard.tsx` — existing empty state pattern to follow
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar layout patterns
- `src/components/LoadingSpinner.tsx` — existing loading indicator (may use Skeleton instead per Figma)
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list (used in selectors)
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selectors allow choosing left and right SBOMs with typeahead search
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare fetches diff data and renders six collapsible sections
- [ ] URL query params update when Compare is clicked, making comparisons shareable
- [ ] Loading with `?left={id1}&right={id2}` in the URL auto-triggers comparison
- [ ] Empty state displays when no comparison is active
- [ ] Loading skeletons display while the API call is in progress
- [ ] Critical vulnerabilities have highlighted/warning row backgrounds
- [ ] Diff sections with >100 items use virtualized rendering
- [ ] Export dropdown is visible (functional export is non-MVP, can be placeholder)

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: selecting two SBOMs and clicking Compare triggers API call
- [ ] Unit test: comparison results render correct sections with expected data
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: sections with zero items are collapsed by default
- [ ] Unit test: URL query params are updated after clicking Compare

## Dependencies
- Depends on: Task 3 — Frontend: API types, client function, and React Query hook for SBOM comparison
