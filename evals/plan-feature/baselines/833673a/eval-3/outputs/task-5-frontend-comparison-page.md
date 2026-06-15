## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page UI at `/sbom/compare` with SBOM selectors, a Compare button, six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state. The page reads `left` and `right` SBOM IDs from URL query parameters to support shareable URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with SBOM selectors, Compare button, and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with a count `Badge` and data `Table`

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` mapping to `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection for SBOMs and a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
**Page structure** follows the page directory pattern in `src/pages/` — each page gets its own directory with a main component and a `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` for the established pattern.

**PatternFly components** (all from PatternFly 5):
- **SBOM selectors**: Use PatternFly `Select` (single, typeahead variant) for both left and right SBOM selectors. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Pre-populate selections from URL query params `left` and `right`.
- **Compare button**: PatternFly primary `Button`, disabled until both selectors have values. On click, update URL query params and trigger the comparison API call via `useSbomComparison` hook.
- **Diff sections**: Each diff category is a PatternFly `ExpandableSection` with a title and count `Badge`. Default expanded for sections with >0 items. Badge colors: green for Added Packages, red for Removed Packages, blue for Version Changes, red for New Vulnerabilities, green for Resolved Vulnerabilities, yellow for License Changes.
- **Data tables**: PatternFly composable `Table` with sortable columns inside each diff section. For >100 rows, use virtualized rendering to prevent browser freezing.
- **New Vulnerabilities table**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the Severity column. Rows with severity "Critical" should have a highlighted background row style.
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Disable the header toolbar during loading.

**URL-shareable comparison**: Use React Router's `useSearchParams` to read/write `left` and `right` query params so comparisons are bookmarkable.

**Route definition**: Add a lazy-loaded route in `src/routes.tsx` following the existing route definition pattern.

**SbomListPage integration**: Add checkbox column to the SBOM table and a "Compare selected" toolbar button. When exactly two SBOMs are checked, navigate to `/sbom/compare?left={id1}&right={id2}`.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — Page structure pattern with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Table component pattern for package data display
- `src/components/SeverityBadge.tsx` — Existing severity badge component to reuse in the New Vulnerabilities table
- `src/components/EmptyStateCard.tsx` — Empty state pattern to reference (though the comparison page uses a standard PatternFly EmptyState)
- `src/components/LoadingSpinner.tsx` — Loading indicator pattern to reference
- `src/components/FilterToolbar.tsx` — Toolbar pattern with PatternFly components
- `src/hooks/useSboms.ts` — Existing hook to populate SBOM selector dropdowns
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping for vulnerability display

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with left and right SBOM selectors
- [ ] Selectors are pre-populated from URL query params `left` and `right`
- [ ] Compare button is disabled until both selectors have values
- [ ] Six diff sections render as collapsible `ExpandableSection` components with count badges
- [ ] Each diff section contains a sortable data table with the correct columns per Figma spec
- [ ] New Vulnerabilities table uses `SeverityBadge` component and highlights Critical rows
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeletons display while API call is in progress
- [ ] URL updates with `left` and `right` query params when a comparison is triggered
- [ ] SbomListPage allows selecting two SBOMs and navigating to the comparison page
- [ ] Diff sections with >0 items are expanded by default; empty sections are collapsed

## Test Requirements
- [ ] Component test: renders empty state when no query params are present
- [ ] Component test: renders loading skeletons while comparison is loading
- [ ] Component test: renders diff sections with correct data when comparison result is available
- [ ] Component test: Compare button is disabled when only one SBOM is selected
- [ ] Component test: Critical severity rows in New Vulnerabilities section have highlighted background

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Frontend API types, client function, and hook

[sdlc-workflow] Description digest: sha256-md:335e8c63c22318d3b0f3cc65d363d7885f1f091a7c9e0c546920bfa4c24d4051
