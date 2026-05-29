# Task 6 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` with a header toolbar (two SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). The page reads SBOM IDs from URL query parameters for shareability and uses PatternFly 5 components throughout, matching the Figma design specifications.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM Select dropdowns, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/VulnerabilityRow.tsx` — Table row component for vulnerability sections with critical severity highlighting

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to the comparison page (lazy-loaded)
- `src/App.tsx` — Verify router setup includes the new route (may already be handled by routes.tsx import)

## Implementation Notes
- **Page structure per Figma design:**
  - Header toolbar at top with two PatternFly `Select` (single, typeahead) dropdowns for SBOM selection. Pre-populate from URL query params `left` and `right`.
  - "Compare" button (primary, disabled until both selectors have values). On click, call `useSbomComparison` hook and update URL query params.
  - "Export" dropdown (secondary, disabled until comparison data is loaded). Two items: "Export JSON" and "Export CSV". Export is a non-MVP feature — implement the dropdown UI but the actual export logic can be a stub that logs a "not implemented" message.
  - Six `ExpandableSection` components stacked vertically, each with a title, count `Badge`, and composable `Table`.

- **Diff sections (in order per Figma):**
  1. Added Packages — green badge, columns: Package Name, Version, License, Advisories (count)
  2. Removed Packages — red badge, columns: Package Name, Version, License, Advisories (count)
  3. Version Changes — blue badge, columns: Package Name, Left Version, Right Version, Direction
  4. New Vulnerabilities — red badge, columns: Advisory ID, Severity (using `SeverityBadge`), Title, Affected Package. Rows with severity "Critical" have highlighted background.
  5. Resolved Vulnerabilities — green badge, columns: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes — yellow badge, columns: Package Name, Left License, Right License

- **Sections default expanded** when they have >0 items, collapsed when empty.

- **Empty state** (no comparison performed yet): PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

- **Loading state**: show PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Disable the header toolbar during loading.

- **URL shareability**: encode both SBOM IDs in URL query params (`?left={id1}&right={id2}`). Use React Router's `useSearchParams` to read/write params. When the page loads with both params present, auto-trigger the comparison.

- **Virtualized lists**: for sections with >100 rows, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.

- Follow the existing page structure pattern in `src/pages/SbomDetailPage/SbomDetailPage.tsx` — each page has its own directory with a main component and `components/` subdirectory.

- Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the SBOM selector dropdowns.

- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display.

- Use the existing `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as a reference for the empty state pattern, or use PatternFly's `EmptyState` directly per the Figma spec.

- Use the existing `LoadingSpinner` from `src/components/LoadingSpinner.tsx` as a reference, but prefer `Skeleton` per the Figma spec.

## Reuse Candidates
- `src/hooks/useSboms.ts` — React Query hook for loading the SBOM list into selector dropdowns
- `src/components/SeverityBadge.tsx` — existing shared component for displaying severity levels in vulnerability tables
- `src/components/EmptyStateCard.tsx` — existing empty state pattern to reference
- `src/components/FilterToolbar.tsx` — existing PatternFly toolbar pattern to reference for the comparison toolbar layout
- `src/components/LoadingSpinner.tsx` — existing loading indicator pattern
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for highlighting critical rows
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component pattern to reference for table column definitions
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list pattern to reference

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns load the SBOM list and allow selection
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare triggers the comparison API call and renders results
- [ ] All six diff sections render with correct columns per Figma specification
- [ ] Each diff section shows a count badge with the correct color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities section highlights rows with Critical severity
- [ ] Empty state renders when no comparison is performed
- [ ] Loading skeletons render during API call
- [ ] URL query params `left` and `right` are updated on comparison and pre-populate selectors on page load
- [ ] Page loads and auto-compares when both URL params are present (shareable URL)

## Test Requirements
- [ ] Unit test: page renders empty state when no SBOM IDs are in URL
- [ ] Unit test: selectors populate with SBOM list from mock data
- [ ] Unit test: comparison results render correctly with all diff sections
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Add comparison mock data fixture to `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison API types, client function, and React Query hook
