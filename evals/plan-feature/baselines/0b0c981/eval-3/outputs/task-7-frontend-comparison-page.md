## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` with a header toolbar containing two SBOM selectors and a Compare button, followed by six collapsible diff sections showing the structured comparison results. The page supports URL-shareable comparisons via `left` and `right` query parameters and includes an empty state when no comparison has been performed.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with `Badge` count and `Table`
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded)

## Implementation Notes
Build the comparison page following the Figma design and existing page patterns:

**Page structure (per `src/pages/` conventions):**
- Create `src/pages/SbomComparePage/` directory with main component, test file, and `components/` subdirectory, mirroring the pattern in `src/pages/SbomDetailPage/`.
- The page is lazy-loaded via React Router following the pattern in `src/routes.tsx`.

**Header toolbar (ComparisonToolbar):**
- Two PatternFly `Select` components (single, typeahead variant) for SBOM selection. Each fetches the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: SBOM name and version (e.g., "my-product-sbom v2.3.1").
- Pre-populate selectors from URL query params `left` and `right` using React Router's `useSearchParams`.
- A primary PatternFly `Button` labeled "Compare" that is disabled until both selectors have values. On click, update the URL query params and trigger the comparison via `useSbomComparison` hook.
- A secondary PatternFly `Dropdown` for export with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.

**Diff sections (DiffSection component):**
- Each section uses a PatternFly `ExpandableSection` with a title and PatternFly `Badge` showing the item count.
- Badge colors per section: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow.
- Sections default to expanded when item count > 0, collapsed when empty.
- Each section contains a PatternFly composable `Table` with sortable columns. For large diffs (>100 rows), use virtualized rendering to prevent browser freezing.

**Section details per Figma design:**
1. **Added Packages** — columns: Package Name, Version, License, Advisories (count). Badge: green.
2. **Removed Packages** — columns: Package Name, Version, License, Advisories (count). Badge: red.
3. **Version Changes** — columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Badge: blue.
4. **New Vulnerabilities** — columns: Advisory ID, Severity (using `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Badge: red. Rows with severity "Critical" get a highlighted background.
5. **Resolved Vulnerabilities** — columns: Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
6. **License Changes** — columns: Package Name, Left License, Right License. Badge: yellow.

**Empty state:**
- When no comparison has been performed (no query params or no data loaded), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed." Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as a reference for the pattern.

**Loading state:**
- While the comparison API is loading, show PatternFly `Skeleton` placeholders in each diff section area. The header toolbar is disabled during loading.

**URL shareability:**
- The page reads `left` and `right` from URL search params on mount. When both are present, the comparison triggers automatically.
- When the user clicks Compare, the URL is updated with `?left={id}&right={id}` enabling bookmarking and sharing.

**Route registration:**
- Add to `src/routes.tsx` following the existing lazy-loaded route pattern. Place the `/sbom/compare` route before `/sbom/:id` to avoid path conflicts.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page structure pattern with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table component pattern for package data display
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in vulnerability sections
- `src/components/EmptyStateCard.tsx` — existing empty state pattern
- `src/components/LoadingSpinner.tsx` — loading indicator pattern (use Skeleton for this page per Figma)
- `src/components/FilterToolbar.tsx` — PatternFly toolbar pattern reference
- `src/hooks/useSboms.ts` — hook for fetching SBOM list used in selectors
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability rows

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selectors load the SBOM list via `useSboms` hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the API call and renders six diff sections
- [ ] Each diff section uses PatternFly `ExpandableSection` with colored `Badge` count
- [ ] Sections with items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities section highlights rows with "Critical" severity
- [ ] Severity badges use the existing `SeverityBadge` component
- [ ] Empty state displays when no comparison is performed
- [ ] Skeleton loading state displays during API call
- [ ] URL query params `left` and `right` enable shareable comparisons
- [ ] Page auto-triggers comparison when both query params are present on load
- [ ] Export dropdown has JSON and CSV options (disabled until data is loaded)
- [ ] Route is registered in `src/routes.tsx` with lazy loading

## Test Requirements
- [ ] Unit test: verify empty state renders when no SBOM IDs are selected
- [ ] Unit test: verify Compare button is disabled when only one SBOM is selected
- [ ] Unit test: verify all six diff sections render with correct data from mock API response
- [ ] Unit test: verify Critical severity rows have highlighted styling
- [ ] Unit test: verify URL query params are read on mount and trigger comparison
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 6 — Add SBOM comparison React Query hook

[sdlc-workflow] Description digest: sha256:717b1b487470fda5d3138ecc84e1bf0f0102897f8b27e41d8f1c1d5d75038760
