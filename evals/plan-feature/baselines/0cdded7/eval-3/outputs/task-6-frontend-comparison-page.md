# Task 6 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selectors and a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), an empty state, and loading state. The URL encodes both SBOM IDs as query parameters for shareability.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (wraps PatternFly `ExpandableSection` with count badge and data table)
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- **PatternFly components to use:**
  - `Select` (single, typeahead) for SBOM selectors — fetch SBOM list via existing `useSboms` hook
  - `ExpandableSection` for each diff section — default expanded for sections with >0 items
  - `Badge` for count badges — colors: green (added, resolved), red (removed, new vulnerabilities), blue (version changes), yellow (license changes)
  - `Table` (composable) for data tables within each section — sortable columns
  - `EmptyState` with `CodeBranchIcon` for the initial state (no comparison performed)
  - `Skeleton` for loading state placeholders
  - `Dropdown` for the Export button with "Export JSON" and "Export CSV" items (Export is non-MVP but UI element should be present and disabled or hidden per feature flag)
- **URL-based state:** Use `useSearchParams` from React Router to read/write `left` and `right` query params. On page load, if both params are present, auto-trigger the comparison. The Compare button updates the URL params, which triggers the `useSbomComparison` hook.
- **Critical vulnerability highlighting:** In the New Vulnerabilities section, rows with severity "Critical" should have a highlighted/danger background. Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display.
- **Virtualized lists:** For diff sections with >100 rows, use virtualized rendering to prevent browser freezing (per NFR). Consider `react-window` or PatternFly's built-in virtualization if available.
- **Page structure:** Follow the existing page directory pattern under `src/pages/` — see `SbomDetailPage/` for a page with sub-components in a `components/` subdirectory.
- Follow the React Router lazy-loading pattern in `src/routes.tsx` for the new route.

**Data component rendering scope:**
- Each diff section table renders data from its corresponding field in the `SbomComparisonResult` response (e.g., Added Packages table renders `result.added_packages`). These are flat arrays, not nested contexts.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability severity display
- `src/components/FilterToolbar.tsx` — reusable toolbar pattern (reference for toolbar layout)
- `src/components/EmptyStateCard.tsx` — existing empty state pattern
- `src/components/LoadingSpinner.tsx` — loading indicator (for loading state)
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page with tabs and sub-components (structural reference)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table component pattern for package data display
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — advisory list component pattern
- `src/hooks/useSboms.ts` — SBOM list hook used to populate the selector dropdowns
- `src/utils/severityUtils.ts` — severity level ordering and color mapping (for Critical row highlighting)

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns allow selecting SBOMs by name/version
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and renders diff sections
- [ ] Six diff sections render with correct titles: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
- [ ] Each section displays a count badge with the correct count and color
- [ ] Sections with >0 items default to expanded; sections with 0 items default to collapsed
- [ ] New Vulnerabilities section highlights rows with Critical severity
- [ ] Empty state displays "Select two SBOMs to compare" when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders while API call is in progress
- [ ] URL query params `left` and `right` encode SBOM IDs for shareability
- [ ] Opening a URL with both params pre-populated auto-triggers comparison
- [ ] Data tables have sortable columns matching the Figma column definitions

## Test Requirements
- [ ] Unit test: render page without query params, verify empty state is shown
- [ ] Unit test: render page with mocked comparison data, verify all six sections render with correct counts
- [ ] Unit test: verify Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: verify Compare button is disabled when only one SBOM is selected
- [ ] Unit test: verify URL params are updated when Compare is clicked
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison data fixture in `tests/mocks/fixtures/sbom-comparison.json`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add frontend API types, client function, and React Query hook for SBOM comparison

[sdlc-workflow] Description digest: sha256:429113cad7169846c4c73456f7d3488c7bf33d99bce376e3700b3d7b6e7fa32f
