## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI based on the Figma design. The page includes a header toolbar with two SBOM selectors and a Compare button, collapsible diff sections for each change category, an empty state for initial page load, and an Export dropdown. The page reads SBOM IDs from URL query parameters for shareability.

## Files to Create
- `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown), six collapsible diff sections, empty state, and loading state
- `src/pages/SbomComparisonPage/components/DiffSection.tsx` — Reusable wrapper component combining PatternFly `ExpandableSection` with a colored `Badge` count and a composable `Table` inside

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparisonPage` (lazy-loaded)

## Implementation Notes
- **Figma-to-PatternFly component mapping**:
  - SBOM selectors: PatternFly `Select` (single, typeahead variant). Pre-populate from URL query params `left` and `right`. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`.
  - Compare button: PatternFly `Button` (variant="primary"), disabled until both selectors have values.
  - Export dropdown: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV"), disabled until comparison data is loaded.
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with count > 0. Each section has a title and a colored `Badge`:
    - Added Packages: green badge
    - Removed Packages: red badge
    - Version Changes: blue badge
    - New Vulnerabilities: red badge
    - Resolved Vulnerabilities: green badge
    - License Changes: yellow badge
  - Data tables: PatternFly `Table` (composable) with sortable columns. For sections with >100 rows, use virtualized rendering.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while API call is in progress. Header toolbar disabled during loading.
  - Severity indicator: reuse `SeverityBadge` from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables.
  - New Vulnerabilities rows with severity "Critical" must have a highlighted background row style.
- **URL shareability**: Read `left` and `right` from `useSearchParams()` (React Router). When the user clicks Compare, update URL search params. This allows bookmarking and sharing comparison URLs.
- **Diff section table columns** (from Figma):
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- Follow existing page structure: each page has its own directory under `src/pages/` with a main component and a `components/` subdirectory (see `src/pages/SbomDetailPage/` as reference).
- Add the route in `src/routes.tsx` following the existing lazy-loaded route pattern.

## Reuse Candidates
- `src/hooks/useSboms.ts` — populates SBOM selector dropdowns with existing SBOM list
- `src/components/SeverityBadge.tsx` — severity level badge for vulnerability tables
- `src/components/EmptyStateCard.tsx` — empty state pattern (adapt for comparison-specific messaging)
- `src/components/LoadingSpinner.tsx` — loading indicator pattern reference
- `src/components/FilterToolbar.tsx` — PatternFly toolbar layout patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table rendering pattern for package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — advisory rendering pattern
- `src/utils/severityUtils.ts` — severity ordering and color mapping for critical row highlighting

## Dependencies
- Depends on: Task 4 — Frontend API layer (useSbomComparison hook, models)

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns populated from `useSboms` hook with typeahead search
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and displays results in six collapsible sections
- [ ] URL updates with `left` and `right` query params when comparison is triggered
- [ ] Page loads comparison directly when opened with `left` and `right` query params in URL
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeleton displays while comparison API call is in progress
- [ ] Sections with count > 0 are expanded by default; sections with count = 0 are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Export dropdown is disabled until comparison data is loaded
- [ ] SeverityBadge component is used in vulnerability diff tables

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors populate with data from useSboms
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: comparison results render correct number of items per diff section
- [ ] Unit test: Critical severity rows have highlighted styling
