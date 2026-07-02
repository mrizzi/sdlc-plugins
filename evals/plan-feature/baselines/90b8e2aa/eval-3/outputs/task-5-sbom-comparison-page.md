## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with a header toolbar containing SBOM selectors, a Compare button, and an Export dropdown. Below the toolbar, render six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) per the Figma design. The URL must encode both SBOM IDs as query parameters for shareable/bookmarkable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component: reads URL query params, renders toolbar and diff sections, manages comparison state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for comparison page component
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with two SBOM Select dropdowns, Compare button, and Export Dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section wrapper with title, count Badge, and configurable data table

## Files to Modify
- `src/routes.tsx` — Add lazy-loaded route for `/sbom/compare` pointing to SbomComparePage

## Implementation Notes
- Follow the existing page structure pattern from `src/pages/SbomListPage/SbomListPage.tsx` for the main page component.
- Follow the page-specific component pattern from `src/pages/SbomDetailPage/components/` for organizing sub-components under the page directory.
- Per the frontend key conventions (Component library): PatternFly 5 — all UI components use PF5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.
- Per the frontend key conventions (Routing): React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript route definition scope.
- Per the frontend key conventions (Page structure): each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.
- Per the frontend key conventions (Testing): Vitest + React Testing Library for unit tests; MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.test.tsx` test file scope.

**Figma design specifications (PatternFly component mapping):**

**Header Toolbar:**
- Left SBOM selector: PatternFly `Select` (single, typeahead variant) — displays SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populated from URL query param `left`. Use the existing `useSboms` hook to fetch the SBOM list for the dropdown options.
- Right SBOM selector: identical PatternFly `Select` (single, typeahead) for the second SBOM. Pre-populated from URL query param `right`.
- Compare button: PatternFly `Button` with `variant="primary"` — disabled until both selectors have values. On click, triggers the comparison API call via `useSbomComparison` hook and updates URL query params.
- Export dropdown: PatternFly `Dropdown` with `variant="secondary"` — two items: "Export JSON" and "Export CSV". Disabled until a comparison result is loaded. (Export functionality is non-MVP but the UI element should be present in disabled state.)

**Diff Sections (six sections, each using PatternFly `ExpandableSection`):**

1. **Added Packages** — packages in right SBOM but not in left.
   - Count Badge: green color
   - Table columns: Package Name, Version, License, Advisories (count)
2. **Removed Packages** — packages in left SBOM but not in right.
   - Count Badge: red color
   - Table columns: Package Name, Version, License, Advisories (count)
3. **Version Changes** — packages in both SBOMs with different versions.
   - Count Badge: blue color
   - Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. **New Vulnerabilities** — advisories affecting right SBOM but not left.
   - Count Badge: red color
   - Table columns: Advisory ID, Severity (using `SeverityBadge` component), Title, Affected Package
   - Rows with severity "Critical" must have a highlighted background (use PatternFly table row variant or custom CSS class)
5. **Resolved Vulnerabilities** — advisories affecting left SBOM but not right.
   - Count Badge: green color
   - Table columns: Advisory ID, Severity, Title, Previously Affected Package
6. **License Changes** — packages with changed licenses between SBOMs.
   - Count Badge: yellow color
   - Table columns: Package Name, Left License, Right License

- Each `ExpandableSection` is default expanded when its item count > 0, default collapsed when empty (0 items).
- Data tables use PatternFly `Table` (composable variant) with sortable columns.
- For large diffs (>100 rows), use virtualized rendering to prevent browser freezing. Consider `react-virtualized` or PatternFly's built-in virtualization support.

**Empty State (no comparison performed yet / page load without query params):**
- PatternFly `EmptyState` component
- Icon: PatternFly `CodeBranchIcon`
- Title: "Select two SBOMs to compare"
- Body: "Choose an SBOM for each side and click Compare to see what changed."

**Loading State (comparison API call in progress):**
- Each diff section shows PatternFly `Skeleton` placeholder
- Header toolbar controls are disabled during loading

**URL-shareable comparison:**
- Use React Router `useSearchParams` to read/write `left` and `right` query parameters
- When the page loads with both params present, auto-trigger the comparison
- When Compare is clicked, update the URL query params so the URL is bookmarkable

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity level badge component for the New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder pattern to follow for the comparison empty state
- `src/components/FilterToolbar.tsx` — existing toolbar layout pattern to reference for the CompareToolbar
- `src/components/LoadingSpinner.tsx` — existing loading indicator pattern
- `src/hooks/useSboms.ts` — existing SBOM list hook for populating the SBOM selector dropdowns
- `src/hooks/useSbomComparison.ts` — comparison data hook from Task 4
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability severity display
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component pattern (column definitions, sorting)
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component pattern

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] SBOM selectors are populated with data from the existing SBOM list endpoint
- [ ] URL query params `left` and `right` pre-populate the respective selectors on page load
- [ ] Compare button triggers the comparison API call and renders diff results in the six sections
- [ ] All six diff sections render with correct PatternFly components, column definitions, and count badges
- [ ] Count badge colors match the Figma specification (green for added/resolved, red for removed/new vulns, blue for version changes, yellow for license changes)
- [ ] Empty state with CodeBranchIcon is shown when no comparison has been performed
- [ ] Loading state with Skeleton placeholders is shown during API call
- [ ] Rows with Critical severity in the New Vulnerabilities section have highlighted background
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] URL is shareable — loading the page with `left` and `right` query params auto-triggers comparison

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders all six diff sections with correct data from mock comparison response
- [ ] Unit test: Compare button is disabled until both SBOM selectors have values
- [ ] Unit test: Compare button is enabled when both selectors have values
- [ ] Unit test: Critical severity vulnerability rows have highlighted background styling
- [ ] Unit test: loading state (Skeleton placeholders) is shown during API call
- [ ] Unit test: empty sections are collapsed, non-empty sections are expanded

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types, REST client function, and React Query hook
