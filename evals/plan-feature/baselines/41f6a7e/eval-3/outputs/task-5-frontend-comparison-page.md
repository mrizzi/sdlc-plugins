# Task 5 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page at `/sbom/compare` per the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. Each section uses PatternFly ExpandableSection with count badges and data tables. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar component with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly ExpandableSection with count badge and data table
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table component for added/removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — table component for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table component for new/resolved vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package) with critical severity row highlighting
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table component for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare` returning mock comparison data
- `tests/mocks/fixtures/sboms.json` — add mock SBOM comparison response fixture data (if needed, or create a new `comparison.json` fixture)

## Implementation Notes
- Follow the existing page structure pattern: each page in its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory.
- Use PatternFly 5 components throughout:
  - `Select` (single, typeahead) for SBOM selectors — pre-populate from URL query params `left` and `right`, fetch SBOM list using existing `useSboms` hook from `src/hooks/useSboms.ts`
  - `ExpandableSection` for each diff category — default expanded when count > 0
  - `Badge` for count indicators with color mapping: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes
  - `Table` (composable) for data tables with sortable columns
  - `EmptyState` with `CodeBranchIcon` when no comparison has been performed
  - `Skeleton` for loading placeholders during API call
  - `Dropdown` for Export button with JSON/CSV options
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display.
- Use `useSbomComparison` hook from Task 4 for the comparison API call.
- URL-shareable: use React Router `useSearchParams` to read/write `left` and `right` query params. When both params are present on page load, auto-trigger the comparison.
- For large diffs (>100 changed packages), use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.
- Rows in the New Vulnerabilities section with severity "Critical" must have a highlighted/emphasized background per the Figma design.
- The Compare button must be disabled until both SBOM selectors have values. The Export dropdown must be disabled until comparison results are loaded.
- The header toolbar must be disabled during loading state.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity level display (Critical/High/Medium/Low)
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder component
- `src/components/LoadingSpinner.tsx` — existing loading indicator component
- `src/components/FilterToolbar.tsx` — existing filter toolbar pattern to reference for toolbar layout
- `src/hooks/useSboms.ts` — existing React Query hook for fetching SBOM list (used in selectors)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component showing the PatternFly Table pattern with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component showing advisory rendering patterns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns are functional with typeahead search, populated from the SBOM list API
- [ ] Compare button triggers the comparison API call and is disabled until both selectors have values
- [ ] URL encodes both SBOM IDs as query parameters (`?left={id1}&right={id2}`) for bookmarking and sharing
- [ ] Opening a URL with both query params auto-triggers the comparison
- [ ] Six collapsible diff sections render with correct data: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
- [ ] Each section displays a count badge with the appropriate color (green/red/blue/yellow per Figma)
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have a highlighted background
- [ ] Existing `SeverityBadge` component is used for vulnerability severity display
- [ ] Empty state shows "Select two SBOMs to compare" with `CodeBranchIcon` when no comparison is active
- [ ] Loading state shows Skeleton placeholders and disables the toolbar
- [ ] Export dropdown has JSON and CSV options and is disabled until results are loaded
- [ ] Large diffs (>100 packages) use virtualized rendering to prevent browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOM IDs are provided
- [ ] Unit test: page renders comparison results after successful API call (mock via MSW)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: Export dropdown is disabled before comparison and enabled after

## Verification Commands
- `npm test -- --run SbomComparePage` — all comparison page unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison
