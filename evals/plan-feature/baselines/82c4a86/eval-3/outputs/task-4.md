# Task 4 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma mockup. The page includes a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown, plus six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section contains a data table with section-specific columns and a color-coded count badge.

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` pointing to the new page component
- `src/App.tsx` — add lazy import for the comparison page (if needed by routing setup)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, Export dropdown

## Implementation Notes
- **Figma compliance**: follow the Figma design exactly for layout, component selection, and interaction patterns.
- **Header toolbar (CompareToolbar)**: use PatternFly `Select` (single, typeahead) for both SBOM selectors. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option (e.g., "my-product-sbom v2.3.1"). Pre-populate selectors from URL query params `left` and `right`. The Compare button is a PatternFly primary `Button`, disabled until both selectors have values. The Export dropdown is a PatternFly `Dropdown` with items "Export JSON" and "Export CSV", disabled until comparison data is loaded.
- **Diff sections (DiffSection)**: each section is a PatternFly `ExpandableSection`. Default expanded when count > 0. Each section has a title and a PatternFly `Badge` showing the item count with section-specific colors:
  - Added Packages: green badge
  - Removed Packages: red badge
  - Version Changes: blue badge
  - New Vulnerabilities: red badge
  - Resolved Vulnerabilities: green badge
  - License Changes: yellow badge
- **Data tables**: use PatternFly composable `Table` with sortable columns. Column definitions per Figma:
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (use existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" get a highlighted background.
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **Virtualization**: for sections with >100 rows, use virtualized list rendering to prevent browser freezing (per non-functional requirements).
- **Empty state**: when no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: while API call is in progress, show PatternFly `Skeleton` in each section area; disable toolbar during loading.
- **URL-shareable**: when Compare is clicked, update the browser URL with `?left={id1}&right={id2}` using React Router's `useSearchParams`. On page load, read params and auto-trigger comparison if both are present.
- **Page structure**: follow existing page pattern — page directory under `src/pages/` with main component, test file, and `components/` subdirectory (see `src/pages/SbomDetailPage/` for reference).
- **Route registration**: add route in `src/routes.tsx` following existing patterns. Register `/sbom/compare` before `/sbom/:id` to avoid path conflicts.
- Per constraints (5.3): follow patterns referenced in Implementation Notes.
- Per constraints (5.4): reuse `SeverityBadge` from `src/components/SeverityBadge.tsx` and `useSboms` from `src/hooks/useSboms.ts` rather than creating new equivalents.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component, use in New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — existing empty state component, adapt for comparison empty state
- `src/components/FilterToolbar.tsx` — existing filter toolbar pattern, reference for toolbar layout
- `src/components/LoadingSpinner.tsx` — existing loading indicator, use as fallback
- `src/hooks/useSboms.ts` — existing hook to populate SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table, reference for table column patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list, reference for advisory display patterns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns populated from SBOM list API
- [ ] Compare button triggers API call and renders diff sections
- [ ] All six diff sections render with correct columns per Figma specification
- [ ] Count badges show correct colors per section (green/red/blue/yellow)
- [ ] Sections with >0 items default to expanded; sections with 0 items default to collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] SeverityBadge component used for severity display in vulnerability sections
- [ ] Empty state shows when no comparison has been performed
- [ ] Loading skeleton shown during API call
- [ ] URL updates with `?left={id}&right={id}` on Compare and is shareable
- [ ] Page loads comparison directly when URL contains both parameters
- [ ] Export dropdown has JSON and CSV options (disabled until data loaded)
- [ ] Large diffs (>100 items per section) use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params present
- [ ] Unit test: selectors populate with SBOM list data
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs selected
- [ ] Unit test: diff sections render correctly with mock comparison data
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted background
- [ ] Unit test: URL is updated when Compare is clicked
- [ ] E2E test: full comparison workflow — select two SBOMs, click Compare, verify diff sections

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — unit tests pass
- `npx tsc --noEmit` — TypeScript compilation passes

## Dependencies
- Depends on: Task 3 — Add comparison API client and React Query hook (provides the data fetching layer this page consumes)
