## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page at `/sbom/compare` with the header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections based on the Figma design. This is the primary UI for the comparison feature, rendering the structured diff returned by the backend. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and data `Table`
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM `Select` dropdowns, Compare button, and Export `Dropdown`

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
- Follow the existing page structure pattern — each page has its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory (see `src/pages/SbomDetailPage/` for reference).
- Follow the React Router v6 lazy-loading pattern used in `src/routes.tsx` for other pages.

**PatternFly component mapping from Figma design:**
- **SBOM selectors**: Use PatternFly `Select` (single, typeahead variant) for both left and right SBOM selection. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option.
- **Compare button**: PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values.
- **Export dropdown**: PatternFly `Dropdown` with `variant="secondary"`. Two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.
- **Diff sections**: Use PatternFly `ExpandableSection` for each category. Default expanded for sections with >0 items, collapsed for empty sections.
- **Count badges**: PatternFly `Badge` inside each section title. Colors: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- **Data tables**: PatternFly `Table` (composable variant) with sortable columns inside each diff section. No pagination — use virtualized rendering for sections with >100 rows (per non-functional requirements).
- **Severity indicators**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display.
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." — displayed when no comparison has been performed.
- **Loading state**: PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress. Disable the header toolbar during loading.

**URL-shareable comparisons:**
- Read `left` and `right` query params from the URL using React Router's `useSearchParams`.
- When both params are present on page load, pre-populate the selectors and automatically trigger the comparison.
- After a comparison is triggered manually, update the URL query params so the URL is shareable.

**New Vulnerabilities highlighting:**
- Rows with severity "Critical" in the New Vulnerabilities section must have a highlighted background (use PatternFly's danger/red row modifier or a CSS class).

**Table columns per section (from Figma):**
1. Added Packages: Package Name, Version, License, Advisories (count)
2. Removed Packages: Package Name, Version, License, Advisories (count)
3. Version Changes: Package Name, Left Version, Right Version, Direction
4. New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes: Package Name, Left License, Right License

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability severity display
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern (may need adaptation for the comparison-specific empty state)
- `src/components/LoadingSpinner.tsx` — existing loading indicator (use Skeleton instead per Figma, but reference this for loading pattern)
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar layout pattern
- `src/hooks/useSboms.ts` — existing hook to fetch SBOM list for the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly Table usage with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory/vulnerability list rendering
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability display

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Both SBOM selectors display available SBOMs loaded via `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and renders diff sections
- [ ] All six diff sections render with correct data tables and column layouts per Figma
- [ ] Each diff section has an `ExpandableSection` with count `Badge` using the correct color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with "Critical" severity have highlighted background
- [ ] Severity is displayed using the existing `SeverityBadge` component
- [ ] Empty state is shown when no comparison has been performed
- [ ] Loading state shows `Skeleton` placeholders during API call
- [ ] URL query params `left` and `right` are updated after comparison and pre-populate on page load
- [ ] Export dropdown appears with JSON and CSV options (disabled until comparison loads)

## Test Requirements
- [ ] Unit test: renders empty state when no comparison is loaded
- [ ] Unit test: renders comparison results with all six diff sections when data is available
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: URL query params are read on mount and trigger comparison
- [ ] Mock the comparison API using MSW handlers in `tests/mocks/handlers.ts`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add comparison API types, client function, and React Query hook
