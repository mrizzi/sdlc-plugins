## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` based on the Figma design context. This is the primary UI surface for the feature: a full-page layout with SBOM selector dropdowns, a "Compare" button, collapsible diff sections with data tables, and empty/loading states. The page reads SBOM IDs from URL query parameters to support URL-shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and vertically stacked diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component wrapping a PatternFly `ExpandableSection` with a colored count `Badge` and a composable `Table`
- `src/pages/SbomComparePage/components/ComparisonEmptyState.tsx` -- Empty state shown before a comparison is performed, using PatternFly `EmptyState` with `CodeBranchIcon`
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Unit tests for the comparison page
- `tests/mocks/fixtures/sbom-comparison.json` -- Mock comparison response data for tests

## Files to Modify
- `src/routes.tsx` -- Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)
- `tests/mocks/handlers.ts` -- Add MSW handler for `GET /api/v2/sbom/compare` returning the mock fixture

## Implementation Notes
- **Figma design compliance** -- The page layout follows the Figma design context exactly:
  - **Header toolbar**: Two PatternFly `Select` components (single-select, typeahead) for SBOM selection. The left selector populates from `left` URL query param; the right from `right`. Use the existing `useSboms` hook (`src/hooks/useSboms.ts`) to fetch the SBOM list for the dropdowns. A primary `Button` labeled "Compare" triggers the API call (disabled until both selectors have values). A secondary `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV" (disabled until comparison data is loaded; export functionality is non-MVP, so the handlers can be stubs).
  - **Diff sections**: Six PatternFly `ExpandableSection` components, each with a title, a colored `Badge` showing the count, and a composable `Table` inside. Section order and badge colors per the Figma spec:
    1. Added Packages -- green badge. Columns: Package Name, Version, License, Advisories (count).
    2. Removed Packages -- red badge. Columns: Package Name, Version, License, Advisories (count).
    3. Version Changes -- blue badge. Columns: Package Name, Left Version, Right Version, Direction.
    4. New Vulnerabilities -- red badge. Columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" must have a highlighted background (use PatternFly `TableComposable` row variant or custom CSS class).
    5. Resolved Vulnerabilities -- green badge. Columns: Advisory ID, Severity, Title, Previously Affected Package.
    6. License Changes -- yellow badge. Columns: Package Name, Left License, Right License.
  - **Empty state**: When no comparison is loaded (no query params), render `ComparisonEmptyState` using PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."
  - **Loading state**: While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- **URL-shareable comparisons**: Use React Router `useSearchParams` to read/write `left` and `right` query parameters. When the user clicks "Compare", update the URL query params so the comparison is bookmarkable. On page load with both params present, auto-trigger the comparison.
- **Virtualized lists**: For diff sections with >100 rows, use `react-window` or PatternFly's built-in virtualization to avoid browser freezing. This addresses the non-functional requirement for large diffs.
- **Route registration**: In `src/routes.tsx`, add the route before the SBOM detail route to avoid path conflicts. Use lazy loading consistent with the existing route pattern:
  ```typescript
  { path: "/sbom/compare", element: <SbomComparePage /> }
  ```
- **DiffSection component**: Extract a reusable `DiffSection` that accepts props: `title`, `badgeColor`, `count`, `columns`, `rows`, `isExpanded` (default: expanded when count > 0). This avoids duplicating the expandable-section-with-table pattern six times.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- Use for severity indicators in the New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` -- Pattern reference for the empty state (though this component uses a different layout, follow the PatternFly `EmptyState` pattern from Figma)
- `src/components/LoadingSpinner.tsx` -- Pattern reference for loading states (use `Skeleton` instead per Figma)
- `src/components/FilterToolbar.tsx` -- Pattern reference for toolbar layout
- `src/hooks/useSboms.ts` -- Fetch SBOM list for the selector dropdowns
- `src/hooks/useSbomComparison.ts` -- Fetch comparison data (created in Task 4)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- Pattern reference for table layout with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` -- Pattern reference for advisory data display

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns load the SBOM list and allow single selection with typeahead
- [ ] "Compare" button is disabled until both SBOMs are selected; clicking it calls the comparison API
- [ ] URL query params `left` and `right` are updated when comparison is triggered
- [ ] Page auto-loads comparison when opened with both query params present
- [ ] Six diff sections render as collapsible `ExpandableSection` components with correct titles and badge colors (green, red, blue, red, green, yellow)
- [ ] Each diff section contains a data table with the correct columns per the Figma spec
- [ ] `SeverityBadge` component is used for severity columns in vulnerability sections
- [ ] Rows with "Critical" severity in New Vulnerabilities section have a highlighted background
- [ ] Empty state renders with `CodeBranchIcon`, correct title and body when no comparison is loaded
- [ ] Skeleton placeholders appear during API loading
- [ ] Export dropdown is present (can be stub handlers for non-MVP)

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders comparison results after successful API call (mock via MSW)
- [ ] Unit test: "Compare" button is disabled when only one SBOM is selected
- [ ] Unit test: critical vulnerabilities row has highlighted styling
- [ ] Unit test: renders loading skeletons while API call is in progress

## Verification Commands
- `npx vitest run SbomComparePage` -- should pass all unit tests

## Dependencies
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
