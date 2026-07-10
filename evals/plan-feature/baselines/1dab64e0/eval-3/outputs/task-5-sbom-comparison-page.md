## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` with the full UI layout from the Figma design. The page includes a header toolbar with SBOM selectors and a Compare button, vertically stacked collapsible diff sections for each change category, and empty/loading states. This is the primary user-facing component of the SBOM comparison feature. The page reads `left` and `right` query parameters from the URL for shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff section rendering
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component using PatternFly `ExpandableSection` with count `Badge` and composable `Table`
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector dropdown component using PatternFly `Select` (single, typeahead) backed by `useSboms` hook

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded `SbomComparePage`

## Implementation Notes
**Figma design implementation:**

The page follows the Figma design layout from the SBOMCompare file (Comparison View page):

**Header toolbar:**
- Two PatternFly `Select` components (single, typeahead variant) for left and right SBOM selection. Each selector shows SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populate from URL query params `left` and `right`. Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to fetch the SBOM list for selector options.
- A primary PatternFly `Button` labeled "Compare" — disabled until both selectors have values. On click, calls `useSbomComparison` with the selected IDs and updates URL query params.
- A secondary PatternFly `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV" — disabled until comparison result is loaded. Client-side download of the already-fetched comparison data.

**Diff sections (six PatternFly `ExpandableSection` components, vertically stacked):**
1. **Added Packages** — PatternFly `Badge` count in green. Composable `Table` columns: Package Name, Version, License, Advisories (count).
2. **Removed Packages** — PatternFly `Badge` count in red. `Table` columns: Package Name, Version, License, Advisories (count).
3. **Version Changes** — PatternFly `Badge` count in blue. `Table` columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
4. **New Vulnerabilities** — PatternFly `Badge` count in red. `Table` columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background (use PatternFly `isHoverable` or custom CSS with `--pf-v5-global--danger-color--100`).
5. **Resolved Vulnerabilities** — PatternFly `Badge` count in green. `Table` columns: Advisory ID, Severity, Title, Previously Affected Package.
6. **License Changes** — PatternFly `Badge` count in yellow. `Table` columns: Package Name, Left License, Right License.

Each `ExpandableSection` is default expanded when its item count > 0, collapsed when empty (0 items).

**Empty state (no comparison performed):**
PatternFly `EmptyState` with `CodeBranchIcon` (PatternFly icon as fallback for ComparisonIcon), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading state:**
PatternFly `Skeleton` placeholders inside each diff section while the comparison API call is in progress. Header toolbar is disabled during loading.

**Virtualized lists:**
For diff sections with >100 items, implement virtualized rendering to prevent browser freezing per the non-functional requirements. Consider `react-window` or PatternFly's built-in virtualization support.

**URL-shareable comparisons:**
Read `left` and `right` query parameters from the URL on page load. When the user clicks "Compare", update the URL query parameters using React Router's `useSearchParams` so the comparison is bookmarkable and shareable.

Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` and `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` page directory scope.

Per CONVENTIONS.md: use PascalCase for component files.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` naming scope.

Per CONVENTIONS.md: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing scope.

Per CONVENTIONS.md: testing uses Vitest + React Testing Library; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` test file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing shared component for severity level display; use in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — Existing empty state component; reference for the comparison empty state pattern
- `src/components/FilterToolbar.tsx` — Existing PatternFly toolbar component; reference for toolbar layout pattern
- `src/components/LoadingSpinner.tsx` — Existing loading indicator; reference for loading state pattern
- `src/hooks/useSboms.ts` — Existing hook for fetching SBOM list; use in SBOM selectors
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — Reference for page component structure with tabs and data display
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Reference for PatternFly composable Table implementation with package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Reference for advisory list rendering pattern

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors load SBOM list and allow typeahead selection
- [ ] Compare button triggers API call and renders diff sections with correct data
- [ ] Each diff section uses PatternFly `ExpandableSection` with colored count `Badge`
- [ ] New Vulnerabilities section highlights rows with severity "Critical"
- [ ] Empty state shows when no comparison has been performed
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query parameters `left` and `right` are read on page load and updated on compare
- [ ] Export dropdown allows client-side JSON and CSV download of comparison data

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: SBOM selectors render with options from mock SBOM data
- [ ] Unit test: Compare button is disabled until both selectors have values
- [ ] Unit test: diff sections render correct data from mock comparison response
- [ ] Unit test: Critical vulnerability rows have highlighted styling
- [ ] Unit test: URL query params are updated when Compare is clicked

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and hook
