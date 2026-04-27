## Repository
trustify-ui

## Description
Create the `SbomComparePage` component at route `/sbom/compare` that provides a side-by-side SBOM comparison view. The page includes SBOM selector dropdowns, a Compare button, expandable diff sections with data tables, and loading/empty states — all built with PatternFly components following the Figma design.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — component tests
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable expandable diff section with badge count and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors and Compare/Export buttons

## Files to Modify
- `src/routes.tsx` — add route `/sbom/compare` pointing to `SbomComparePage`

## Implementation Notes
- **PatternFly components from Figma design**:
  - SBOM selectors: PatternFly `Select` (single, typeahead) — pre-populate from URL query params `left` and `right`, load SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`
  - Compare button: PatternFly `Button` (primary), disabled until both selectors have values
  - Export dropdown: PatternFly `Dropdown` with "Export JSON" and "Export CSV" items
  - Diff sections: PatternFly `ExpandableSection` — one per diff category, default expanded when count > 0
  - Count badges: PatternFly `Badge` — green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes
  - Data tables: PatternFly `Table` (composable) with sortable columns
  - Severity display: reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare"
  - Loading state: PatternFly `Skeleton` placeholders in each diff section
- Use React Router `useSearchParams` for URL-shareable comparison (encode both SBOM IDs in URL query params).
- For large diffs (>100 rows), use virtualized rendering to prevent browser freezing.
- Follow the page structure convention: page directory under `src/pages/` with main component, test file, and `components/` subdirectory.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability display
- `src/components/EmptyStateCard.tsx` — existing empty state pattern
- `src/components/FilterToolbar.tsx` — reference for toolbar layout patterns
- `src/hooks/useSboms.ts` — existing hook for loading SBOM list in selectors
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page layout with tabs/sections

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Two SBOM selector dropdowns allow selecting SBOMs by name/version
- [ ] Compare button triggers API call and renders diff sections
- [ ] Six diff sections display with correct data tables and badge counts
- [ ] Critical vulnerability rows have highlighted background
- [ ] URL encodes both SBOM IDs for bookmarking/sharing
- [ ] Empty state shows when no comparison is loaded
- [ ] Loading skeletons display while API call is in progress

## Test Requirements
- [ ] Component test: renders empty state on initial load
- [ ] Component test: renders diff sections after successful comparison
- [ ] Component test: severity badges display correctly for vulnerability rows
- [ ] Component test: URL params populate SBOM selectors
- [ ] E2E test: full comparison workflow from SBOM selection to diff display

## Dependencies
- Depends on: Task 4 — Frontend API client and hook
