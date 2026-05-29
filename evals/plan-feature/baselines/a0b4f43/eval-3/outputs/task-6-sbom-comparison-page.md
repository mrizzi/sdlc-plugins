## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page at `/sbom/compare` with a header toolbar for SBOM selection and collapsible diff sections displaying the comparison results. The page uses PatternFly components as specified in the Figma design and integrates with the comparison API hook. Register the route in the application router.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar component with two SBOM Select dropdowns, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection with count Badge and data Table

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to lazy-loaded SbomComparePage
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the SBOM table and a "Compare selected" toolbar action that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Figma component mapping** (PatternFly 5):
  - SBOM selectors: PatternFly `Select` (single, typeahead variant) — fetches SBOM list via existing `useSboms` hook. Pre-populate from URL query params `left` and `right`.
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items, collapsed for empty sections.
  - Count badges: PatternFly `Badge` — green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
  - Data tables: PatternFly `Table` (composable) — sortable columns. Use virtualized rendering (e.g., react-window or PatternFly's built-in virtualization) for sections with >100 rows to prevent browser freezing.
  - Severity indicator: Reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Export button: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded.
  - Loading state: PatternFly `Skeleton` placeholder in each diff section while the comparison API call is in progress. Header toolbar disabled during loading.

- **Diff section table columns** (from Figma):
  1. Added Packages: Package Name, Version, License, Advisories (count)
  2. Removed Packages: Package Name, Version, License, Advisories (count)
  3. Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  4. New Vulnerabilities: Advisory ID, Severity (using SeverityBadge), Title, Affected Package — rows with severity "Critical" have a highlighted background (use PatternFly `isHoverable` or custom row class)
  5. Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  6. License Changes: Package Name, Left License, Right License

- **URL-shareable comparison**: Read `left` and `right` query parameters from the URL on page load. If both are present, auto-trigger the comparison. When the user clicks Compare, update the URL query params using React Router's `useSearchParams` so the URL is always bookmarkable.

- **Compare button**: Disabled until both SBOM selectors have values. Clicking it updates URL params and triggers the comparison hook.

- **Export functionality**: Export is MVP-excluded per requirements but the Export dropdown should be rendered in disabled state as a placeholder for future implementation.

- **SbomListPage integration**: Add a checkbox column to the existing SBOM table using PatternFly's `isSelectableRow` pattern. Add a toolbar action "Compare selected" that is enabled when exactly 2 SBOMs are checked. Clicking it navigates to `/sbom/compare?left={id1}&right={id2}`.

- Follow the existing page structure convention: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` for the established pattern.

- Use React Router v6 `useSearchParams` for reading/writing URL query parameters.

- Use lazy loading for the new page component in route registration, following the existing pattern in `src/routes.tsx`.

**Data component rendering scope:**
- All six diff section tables render **per-comparison** data scoped to the selected left/right SBOM pair. Each table displays the corresponding array from the single `SbomComparisonResult` response — no cross-comparison aggregation.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing shared component for severity display; reuse in New Vulnerabilities and Resolved Vulnerabilities tables
- `src/components/FilterToolbar.tsx` — Existing reusable filter toolbar; reference for PatternFly toolbar patterns
- `src/components/EmptyStateCard.tsx` — Existing empty state component; reference for empty state pattern (may use directly or adapt)
- `src/components/LoadingSpinner.tsx` — Existing loading indicator; reference for loading state pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Existing package table component; reference for PatternFly Table column definition and row rendering patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Existing advisory list component; reference for advisory data rendering
- `src/hooks/useSboms.ts` — Use to populate the SBOM selector dropdowns with available SBOMs

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] SBOM selectors populate from the SBOM list API and support typeahead filtering
- [ ] URL query params `left` and `right` are read on page load and pre-populate the selectors
- [ ] Clicking Compare updates the URL and displays the structured diff
- [ ] All six diff sections render with correct table columns and count badges
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state shows when no comparison has been performed
- [ ] Loading skeletons appear while the comparison API call is in progress
- [ ] SbomListPage has checkbox selection and "Compare selected" action navigating to comparison page
- [ ] Route is registered in `src/routes.tsx` with lazy loading

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are present
- [ ] Unit test: SbomComparePage renders diff sections with correct data when comparison result is loaded (mock via MSW)
- [ ] Unit test: CompareToolbar disables Compare button when fewer than 2 SBOMs are selected
- [ ] Unit test: DiffSection renders as expanded when item count > 0 and collapsed when count = 0
- [ ] Unit test: New Vulnerabilities table applies highlighted row style for Critical severity
- [ ] Unit test: SbomListPage "Compare selected" button navigates to correct URL with both SBOM IDs

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 5 — Add API types, client function, and React Query hook for SBOM comparison (trustify-ui)