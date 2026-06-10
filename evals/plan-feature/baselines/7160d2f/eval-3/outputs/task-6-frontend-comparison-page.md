## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page UI with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections for each change category. This is the main user-facing component of the SBOM comparison feature, rendering the comparison data fetched via the API layer from Task 5. The page uses PatternFly components throughout, matching the Figma design specifications.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the new comparison page

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and data `Table`
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM `Select` dropdowns, Compare `Button`, and Export `Dropdown`

## Implementation Notes
Follow the existing page structure pattern in `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` — each page gets its own directory with a main component file, test file, and `components/` subdirectory for page-specific components.

**Figma design — PatternFly component mapping:**
- SBOM selectors: PatternFly `Select` (single, typeahead variant) — fetches SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`. Pre-populate from URL query params `left` and `right`.
- Compare button: PatternFly `Button` (primary variant) — disabled until both selectors have values. Triggers `useSbomComparison` hook from Task 5.
- Export button: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV") — disabled until comparison result is loaded.
- Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items, collapsed for empty sections. Each section has a title and count `Badge`.
- Data tables inside sections: PatternFly `Table` (composable variant) with sortable columns. For >100 rows, use virtualized rendering to prevent browser freezing per the non-functional requirements.
- Severity indicators in "New Vulnerabilities" and "Resolved Vulnerabilities" sections: use existing `SeverityBadge` shared component from `src/components/SeverityBadge.tsx`.
- Empty state (no comparison performed): PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Follow the pattern in `src/components/EmptyStateCard.tsx`.
- Loading state: PatternFly `Skeleton` placeholder in each diff section while API call is in progress. Disable header toolbar during loading.

**Diff section specifications (from Figma):**
1. Added Packages — columns: Package Name, Version, License, Advisories (count). Badge color: green.
2. Removed Packages — columns: Package Name, Version, License, Advisories (count). Badge color: red.
3. Version Changes — columns: Package Name, Left Version, Right Version, Direction. Badge color: blue.
4. New Vulnerabilities — columns: Advisory ID, Severity (SeverityBadge), Title, Affected Package. Badge color: red. Rows with severity "Critical" have highlighted background.
5. Resolved Vulnerabilities — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge color: green.
6. License Changes — columns: Package Name, Left License, Right License. Badge color: yellow.

**URL-shareable comparison:**
Read `left` and `right` query parameters from the URL on page load and pre-populate the SBOM selectors. When the user clicks Compare, update the URL query parameters using React Router's `useSearchParams` so the comparison is bookmarkable and shareable.

**Route registration:**
Add to `src/routes.tsx` following the existing lazy-loaded page pattern (e.g., how `SbomListPage`, `SbomDetailPage` are registered). The route path should be `/sbom/compare`.

**Data component rendering scope:**
All six diff section tables render data from a single comparison result — they are not per-context (no wizard/tab nesting). Each table displays the full list for its category from the `SbomComparison` response.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in vulnerability diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern to follow for the "no comparison" state
- `src/components/FilterToolbar.tsx` — reusable filter toolbar pattern (may inform CompareToolbar structure)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (Skeleton is preferred here per Figma but this shows the pattern)
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component showing PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component showing advisory data display patterns
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list (used by the selector dropdowns)

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns load the SBOM list and allow selection
- [ ] Compare button triggers the comparison API call and renders diff sections
- [ ] All six diff sections display with correct columns, count badges, and badge colors per Figma
- [ ] "New Vulnerabilities" rows with Critical severity have highlighted background
- [ ] Severity indicators use the existing `SeverityBadge` component
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query parameters are updated on Compare and read on page load (shareable URLs)
- [ ] Export dropdown is present and disabled until comparison is loaded

## Test Requirements
- [ ] Unit test: render comparison page with no query params — verify empty state is shown
- [ ] Unit test: render comparison page with mock comparison data — verify all six diff sections render with correct data
- [ ] Unit test: verify Critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: verify Compare button is disabled until both SBOM selectors have values
- [ ] Unit test: verify Export dropdown is disabled until comparison result is loaded
- [ ] Unit test: verify URL parameters are updated when Compare is clicked

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 5 — Add frontend API layer for SBOM comparison
