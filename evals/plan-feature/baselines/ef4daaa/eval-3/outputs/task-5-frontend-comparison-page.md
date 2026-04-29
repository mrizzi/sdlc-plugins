# Task 5 — Frontend SBOM comparison page

## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via query parameters.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to `SbomComparePage`
- `src/App.tsx` — add lazy import for the new page component (if not handled by routes.tsx)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component with count badge and data table
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table for added/removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table for new/resolved vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table for license changes (columns: Package Name, Left License, Right License)

## Implementation Notes
- **Page structure pattern**: follow the page directory structure used by `src/pages/SbomDetailPage/` — a main page component with a `components/` subdirectory for page-specific sub-components.
- **Header toolbar**:
  - Two PatternFly `Select` components (single, typeahead) for SBOM selection. Pre-populate from URL query params `left` and `right`. Use the existing `useSboms` hook (`src/hooks/useSboms.ts`) to fetch the SBOM list for the dropdown options.
  - "Compare" primary button — disabled until both selectors have values. On click, update URL query params and trigger the `useSbomComparison` hook (from Task 4).
  - "Export" secondary `Dropdown` with "Export JSON" and "Export CSV" items — disabled until comparison data is loaded. (Export is non-MVP; implement as disabled placeholder or functional if time permits.)
- **URL-shareable comparison**: use React Router's `useSearchParams` to read/write `left` and `right` query parameters. When the page loads with both params, auto-trigger the comparison.
- **Diff sections**: use PatternFly `ExpandableSection` for each category. Each section has:
  - Title with count `Badge` (color: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes)
  - Sections with >0 items are expanded by default; sections with 0 items are collapsed
  - PatternFly composable `Table` inside each section with sortable columns
- **New Vulnerabilities section**: rows with severity "Critical" should have a highlighted background (use PatternFly `isHoverable` or custom row class with `--pf-v5-global--danger-color--100` background).
- **Virtualized lists**: for diff sections with >100 items, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.
- **Empty state**: when no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: while the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- **Existing shared components to use**:
  - `src/components/SeverityBadge.tsx` — for severity display in vulnerability tables
  - `src/components/LoadingSpinner.tsx` — for general loading states
  - `src/components/EmptyStateCard.tsx` — reference for empty state pattern (though the comparison empty state has specific content)
- **Route registration**: add to `src/routes.tsx` following the existing pattern. Ensure `/sbom/compare` is registered before `/sbom/:id` to avoid route conflicts.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page structure pattern with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table component pattern for package data display
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — advisory rendering pattern
- `src/components/SeverityBadge.tsx` — severity badge component for vulnerability tables
- `src/components/EmptyStateCard.tsx` — empty state pattern reference
- `src/components/FilterToolbar.tsx` — toolbar pattern reference
- `src/hooks/useSboms.ts` — SBOM list fetching for selector dropdowns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability highlight logic
- `src/routes.tsx` — route definition pattern to follow

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] SBOM selector dropdowns load and display available SBOMs
- [ ] "Compare" button triggers comparison API call when both SBOMs are selected
- [ ] URL encodes both SBOM IDs as query parameters (`?left={id1}&right={id2}`)
- [ ] Page loads comparison directly when opened with both query params (URL-shareable)
- [ ] All six diff sections render with correct data, count badges, and color coding
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Critical vulnerabilities have highlighted background in New Vulnerabilities section
- [ ] Empty state displays when no comparison is performed
- [ ] Loading skeletons display while comparison is in progress
- [ ] Toolbar is disabled during loading
- [ ] Large diffs (>100 items) render without browser freezing (virtualized lists)

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page auto-triggers comparison when both query params are in the URL
- [ ] Unit test: "Compare" button is disabled when only one SBOM is selected
- [ ] Unit test: diff sections render with correct data from mock API response
- [ ] Unit test: sections with 0 items are collapsed, sections with >0 items are expanded
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: Export dropdown is disabled when no comparison data is loaded

## Dependencies
- Depends on: Task 4 — Frontend API client and React Query hook for SBOM comparison
