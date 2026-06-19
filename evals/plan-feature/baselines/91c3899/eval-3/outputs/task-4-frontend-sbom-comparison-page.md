# Task 4 — Add SBOM comparison page

## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown, plus six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section contains a data table with sortable columns. The page reads SBOM IDs from URL query parameters for shareability and uses the useSbomComparison hook from Task 3 for data fetching.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping ExpandableSection + Badge + Table

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)

## Implementation Notes
- Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory. See `src/pages/SbomDetailPage/` for the established pattern.

**Figma design — PatternFly component mapping:**

- **SBOM selectors:** Use PatternFly `Select` (single, typeahead variant) for both left and right SBOM dropdowns. Pre-populate from URL query params `left` and `right`. Fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
- **Compare button:** PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values. On click, update URL query params and trigger the comparison API call via `useSbomComparison`.
- **Export dropdown:** PatternFly `Dropdown` with `variant="secondary"`. Two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.
- **Diff sections:** Each section uses PatternFly `ExpandableSection` with a title and a PatternFly `Badge` showing the item count. Sections with >0 items default to expanded. Badge colors per section:
  - Added Packages: green
  - Removed Packages: red
  - Version Changes: blue
  - New Vulnerabilities: red
  - Resolved Vulnerabilities: green
  - License Changes: yellow
- **Data tables:** PatternFly `Table` (composable) with sortable columns inside each diff section. No pagination — use virtualized rendering for sections with >100 rows to meet the non-functional requirement of handling large diffs without browser freezing.
- **New Vulnerabilities table:** Rows with severity "Critical" must have a highlighted background (use PatternFly's `isRowSelected` or custom row class). Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the Severity column.
- **Empty state:** When no comparison has been performed (page loaded without query params or before clicking Compare), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state:** While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.

**Table columns per section (from Figma):**
1. Added Packages: Package Name, Version, License, Advisories (count)
2. Removed Packages: Package Name, Version, License, Advisories (count)
3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
4. New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
6. License Changes: Package Name, Left License, Right License

**URL shareability:** Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. When query params are present on page load, auto-populate the selectors and trigger the comparison.

- Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/` directory matching the convention's page directory scope.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's route definition file scope.
- Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities, kebab-case for directories.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TypeScript/React file scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for rendering severity levels (Critical/High/Medium/Low); use in the New Vulnerabilities and Resolved Vulnerabilities table columns
- `src/components/EmptyStateCard.tsx` — existing empty state component; evaluate whether it can be used or adapted for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; may be useful alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — existing reusable filter toolbar with PatternFly; reference its PatternFly Select usage patterns
- `src/hooks/useSboms.ts` — existing hook for fetching SBOM list; reuse for populating the SBOM selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference its PatternFly Table usage for the diff section tables
- `src/utils/severityUtils.ts` — existing severity level ordering and color mapping utilities; reuse for sorting and styling vulnerability entries

## Acceptance Criteria
- [ ] Page renders at /sbom/compare with all Figma-specified UI elements
- [ ] Both SBOM selector dropdowns are populated with available SBOMs via useSboms hook
- [ ] Compare button triggers the comparison API call and renders results in six collapsible sections
- [ ] Each diff section shows correct count badge with the Figma-specified color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] SeverityBadge component is used for severity display in vulnerability sections
- [ ] Empty state is shown when no comparison has been performed
- [ ] Skeleton loading state is shown during API call
- [ ] URL query parameters (left, right) are updated on Compare and read on page load for shareability
- [ ] Large diffs (>100 rows per section) use virtualized rendering

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders comparison results with correct section titles and count badges
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: Compare button is disabled when one or both selectors are empty
- [ ] Unit test: Export dropdown is disabled when no comparison data is loaded
- [ ] Unit test: SBOM selectors are pre-populated from URL query params

## Dependencies
- Depends on: Task 3 — Add SBOM comparison API layer
