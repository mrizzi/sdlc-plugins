# TC-9003-5: Frontend comparison page and diff section components

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Build the SBOM comparison page at `/sbom/compare` with a header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections for each change category. This is the primary UI deliverable of the feature, translating the Figma design into PatternFly 5 components with React Query data binding.

## Files to Create

- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component (wraps PatternFly `ExpandableSection` + `Table`)
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify

- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `SbomComparePage`

## Dependencies

- TC-9003-4 (API types and `useSbomComparison` hook must exist)

## Implementation Notes

### Figma Design Reference

The page layout follows the Figma design context (SBOMCompare mockup):

**Header Toolbar (`ComparisonToolbar.tsx`)**:
- Two PatternFly `Select` components (single-select, typeahead variant) for left and right SBOM selection. These should fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Pre-populate from URL query params `left` and `right`.
- A primary PatternFly `Button` labeled "Compare", disabled until both selectors have values. On click, triggers the `useSbomComparison` hook by updating the selected IDs.
- A secondary PatternFly `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV". Disabled until comparison data is loaded.

**Diff Sections (`DiffSection.tsx`)**:
- Each section is a PatternFly `ExpandableSection` with a title and a PatternFly `Badge` showing the item count. Badge colors per the Figma spec: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- Sections default to expanded when they contain items (count > 0) and collapsed when empty.
- Inside each section, a PatternFly `Table` (composable variant) displays the diff data with sortable columns. For sections with >100 rows, implement virtualized rendering to meet the NFR for large diffs.
- The "New Vulnerabilities" section table rows with severity "Critical" should have a highlighted background row style.
- Severity values in the New Vulnerabilities and Resolved Vulnerabilities tables should use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`.

**Section order** (per Figma): Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.

**Empty State**: When no comparison has been performed (no query params, or selectors not yet filled), render a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as a pattern reference.

**Loading State**: While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading using the `LoadingSpinner` pattern from `src/components/LoadingSpinner.tsx`.

**URL Synchronization**: When the user clicks Compare, update the browser URL to `/sbom/compare?left={id1}&right={id2}` using React Router's `useSearchParams`. On page load, read `left` and `right` from URL params to support shareable/bookmarkable comparisons.

### Route Registration
- Add a lazy-loaded route in `src/routes.tsx` for path `/sbom/compare` mapping to `SbomComparePage`, following the existing pattern for `SbomListPage` and `SbomDetailPage`.

## Acceptance Criteria

- [ ] Comparison page renders at `/sbom/compare`
- [ ] SBOM selectors load SBOM list from the existing API
- [ ] Compare button triggers comparison and displays results in collapsible sections
- [ ] Each diff section shows correct count badge with appropriate color
- [ ] New Vulnerabilities section highlights Critical rows
- [ ] Severity badges render using the existing `SeverityBadge` component
- [ ] Empty state displays when no comparison is active
- [ ] Loading skeletons display during API call
- [ ] URL updates with `left` and `right` params for shareability
- [ ] Page loads comparison directly when URL params are present
- [ ] Export dropdown is present and disabled until data loads

## Test Requirements

- [ ] Unit test: page renders empty state when no SBOM IDs are provided
- [ ] Unit test: page renders diff sections with mock comparison data (MSW handler)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: Critical vulnerability rows have highlighted styling
- [ ] Unit test: URL params are read on mount and pre-populate the selectors

## Reuse Candidates

- `src/components/SeverityBadge.tsx` — Severity level badge for vulnerability tables
- `src/components/EmptyStateCard.tsx` — Empty state pattern reference
- `src/components/LoadingSpinner.tsx` — Loading state pattern reference
- `src/hooks/useSboms.ts` — SBOM list fetching for the selector dropdowns

## Convention Compliance

- `Applies: task creates src/pages/SbomComparePage/SbomComparePage.tsx matching the convention's page structure scope (each page gets its own directory under src/pages/).`
- `Applies: task creates src/pages/SbomComparePage/components/DiffSection.tsx and ComparisonToolbar.tsx matching the convention's page-specific components scope (components/ subdirectory).`
- `Applies: task modifies src/routes.tsx matching the convention's routing scope (React Router v6 with lazy-loaded page components).`

[Description digest: sha256-md:e7b1a5c3d0f6b2e8a4d9c5f1b7e3a0d6c2f8b4e1a7d3c9f5b0e6a2d8c4f0b7e3]
