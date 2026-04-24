# Task 4 — Frontend SBOM comparison page with diff sections

## Repository
trustify-ui

## Description
Build the full SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selector dropdowns and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), an empty state for when no comparison has been performed, and a loading state with skeleton placeholders. The page reads SBOM IDs from URL query parameters (`left` and `right`) to support URL-shareable comparisons.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the new page component

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar, SBOM selectors, compare button, and diff section container
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (PatternFly `ExpandableSection` with `Badge` count and `Table`)
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar component with SBOM selectors and action buttons

## Implementation Notes
- Follow the existing page structure pattern: each page has its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory. See `src/pages/SbomDetailPage/` for reference.
- **Route registration**: add a lazy-loaded route in `src/routes.tsx` for `/sbom/compare` following the existing route definition pattern (React Router v6 with lazy loading).
- **URL-driven state**: read `left` and `right` SBOM IDs from URL query parameters using React Router's `useSearchParams()`. When the user clicks Compare, update the URL query params so the comparison is bookmarkable and shareable (UC-2 requirement).
- **SBOM selectors**: use PatternFly 5 `Select` components with single-select typeahead. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: `"{name} {version}"`.
- **Compare button**: PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values. On click, update URL query params with selected IDs, which triggers `useSbomComparison` hook (from Task 3).
- **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. This is a non-MVP feature — implement as disabled placeholder buttons for now.
- **Diff sections**: use the `DiffSection` reusable component for all six sections. Each `DiffSection` wraps PatternFly `ExpandableSection` with:
  - Title (e.g., "Added Packages")
  - `Badge` count with color: green for Added/Resolved, red for Removed/New Vulnerabilities, blue for Version Changes, yellow (gold) for License Changes
  - PatternFly `Table` (composable) with sortable columns
  - Sections default to expanded when they have >0 items, collapsed when empty (0 items)
- **Table columns per section** (from Figma design):
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Critical vulnerability highlighting**: rows in the New Vulnerabilities section where severity is "Critical" should have a highlighted background (use PatternFly danger/critical row variant or a CSS class).
- **Virtualized lists**: for sections with >100 rows, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.
- **Empty state**: when no comparison has been performed (no query params), render PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: while the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- Component library: all UI elements must use PatternFly 5 components — no custom HTML for standard UI patterns.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing component for rendering severity indicators; reuse in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state component; review for reuse or follow its pattern for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; may be useful alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — existing reusable toolbar component; review for partial reuse in the comparison toolbar
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list; reuse for populating selector dropdowns
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page structure with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage with package data
- `src/utils/severityUtils.ts` — existing severity level ordering and color mapping; reuse for severity-related display logic

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns load the list of available SBOMs
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare updates URL query params and triggers the comparison API call
- [ ] All six diff sections render with correct data tables and column definitions
- [ ] Diff sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Count badges display correct counts with appropriate colors (green/red/blue/yellow)
- [ ] Critical vulnerabilities in New Vulnerabilities section have highlighted row backgrounds
- [ ] Empty state displays when no comparison has been performed (page load without query params)
- [ ] Loading skeleton placeholders display while the comparison API is in progress
- [ ] URL with `left` and `right` query params loads the comparison directly (shareable URLs)
- [ ] Large diffs (>100 rows) render without browser freezing (virtualization)

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders SBOM selectors and disabled Compare button on load
- [ ] Unit test: Compare button becomes enabled when both SBOMs are selected
- [ ] Unit test: comparison results render correct number of diff sections with correct counts
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: page renders loading state with skeletons during API call
- [ ] Unit test: page pre-populates selectors and triggers comparison when URL has query params
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison result fixture in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 3 — Frontend API layer, types, and React Query hook for SBOM comparison
