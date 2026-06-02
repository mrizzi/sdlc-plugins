## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page UI at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly data tables. The page supports an empty state when no comparison has been performed and a loading state with skeleton placeholders while the API call is in progress.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable diff section component wrapping PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar component with SBOM Select dropdowns, Compare button, and Export Dropdown

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` mock responses
- `tests/mocks/fixtures/sboms.json` — Add mock SBOM comparison result fixture data

## Implementation Notes
**Figma component mapping — use these PatternFly 5 components:**

- **SBOM selectors**: PatternFly `Select` component (single selection, typeahead variant) for both left and right SBOM selection. Pre-populate from URL query params `left` and `right`. Fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1") in each option.

- **Compare button**: PatternFly primary action button, disabled until both selectors have values. On click, trigger the comparison by calling the `useSbomComparison` hook with the selected IDs.

- **Export dropdown**: PatternFly `Dropdown` component as a secondary button with two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded.

- **Diff sections**: Each section uses PatternFly `ExpandableSection` with a title and a count `Badge`. Sections default to expanded when they have >0 items. Six sections in order:
  1. **Added Packages** — Badge color: green. Table columns: Package Name, Version, License, Advisories (count).
  2. **Removed Packages** — Badge color: red. Table columns: Package Name, Version, License, Advisories (count).
  3. **Version Changes** — Badge color: blue. Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
  4. **New Vulnerabilities** — Badge color: red. Table columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background.
  5. **Resolved Vulnerabilities** — Badge color: green. Table columns: Advisory ID, Severity, Title, Previously Affected Package.
  6. **License Changes** — Badge color: yellow. Table columns: Package Name, Left License, Right License.

- **Data tables**: PatternFly `Table` (composable) with sortable columns. No pagination — use virtualized rendering for lists with >100 rows to prevent browser freezing per the non-functional requirement.

- **Empty state**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."

- **Loading state**: While the comparison API call is in progress, each diff section shows a PatternFly `Skeleton` placeholder. The header toolbar is disabled during loading.

- **Critical vulnerability highlighting**: In the New Vulnerabilities section, rows where `severity` is "Critical" must have a visually highlighted background. Use the existing severity utilities in `src/utils/severityUtils.ts` for severity ordering and color mapping.

Follow the page structure pattern established in `src/pages/SbomListPage/SbomListPage.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.tsx` — each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory.

For testing, follow the Vitest + React Testing Library pattern in `src/pages/SbomListPage/SbomListPage.test.tsx`. Use MSW handlers from `tests/mocks/handlers.ts` for API mocking. Add fixture data in `tests/mocks/fixtures/sboms.json`.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing severity badge component; use directly in the New Vulnerabilities and Resolved Vulnerabilities table columns
- `src/components/EmptyStateCard.tsx` — Existing empty state component; adapt for the comparison empty state or use PatternFly EmptyState directly per the Figma design
- `src/components/LoadingSpinner.tsx` — Existing loading indicator; reference for loading state patterns
- `src/components/FilterToolbar.tsx` — Existing toolbar component; reference for PatternFly toolbar layout patterns
- `src/hooks/useSboms.ts` — Existing hook for fetching SBOM list; use directly in SBOM selector dropdowns
- `src/utils/severityUtils.ts` — Existing severity level ordering and color mapping utilities; use for critical vulnerability highlighting
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing page component; follow the same page structure pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table; reference for PatternFly Table usage with package data

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] Left and right SBOM selector dropdowns load SBOM list and support typeahead search
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers API call and renders diff sections with results
- [ ] All six diff sections render with correct column layouts and count badges
- [ ] Sections with >0 items default to expanded; sections with 0 items default to collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state displays when page loads without query params
- [ ] Loading state shows skeleton placeholders while API call is in progress
- [ ] Export dropdown has JSON and CSV options, disabled until comparison result is loaded
- [ ] SeverityBadge component is used for severity display in vulnerability sections
- [ ] Large diffs (>100 rows) use virtualized rendering to prevent browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOM IDs are provided
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Compare button is enabled when both SBOMs are selected
- [ ] Unit test: clicking Compare triggers API call and renders diff sections
- [ ] Unit test: added packages section displays correct count badge and table data
- [ ] Unit test: critical vulnerabilities have highlighted row styling
- [ ] Unit test: loading state shows skeleton placeholders

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API client and React Query hook
