# Task 6: Create SBOM comparison page with Figma design

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page component and its sub-components, following the Figma design specifications. The page includes a header toolbar with SBOM selectors and a Compare button, six collapsible diff sections with count badges and data tables, an empty state for initial load, and skeleton loading states during API calls. The route is registered at `/sbom/compare` with URL query parameters for shareable comparisons.

## Figma Design Reference
The Figma design (file `SBOMCompare`, page `Comparison View`) specifies the following PatternFly component mapping and visual requirements:

- **SBOM selectors**: PatternFly `Select` (single, typeahead) — pre-populated from URL query params `left` and `right`, fetches SBOM list via existing `useSboms` hook
- **Diff sections**: PatternFly `ExpandableSection` — default expanded for sections with >0 items, collapsed for empty sections
- **Count badges**: PatternFly `Badge` with section-specific colors:
  - Added Packages: **green**
  - Removed Packages: **red**
  - Version Changes: **blue**
  - New Vulnerabilities: **red**
  - Resolved Vulnerabilities: **green**
  - License Changes: **yellow**
- **Data tables**: PatternFly `Table` (composable) — sortable columns, no pagination (virtualized for >100 rows)
- **Severity indicators**: Existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` — used in New/Resolved Vulnerabilities tables. Rows with severity "Critical" have a **highlighted background**
- **Empty state**: PatternFly `EmptyState` — shown when no comparison has been performed; icon: `CodeBranchIcon`, title: "Select two SBOMs to compare", body: "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress; header toolbar disabled during loading
- **Export button**: PatternFly `Dropdown` with items "Export JSON" and "Export CSV", disabled until comparison result is loaded

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and vertically stacked collapsible diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page (rendering, section expansion, empty state, loading state)
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component that wraps `ExpandableSection` with a `Badge` count and a `Table` for diff data
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector dropdown component using PatternFly `Select` with typeahead, backed by the `useSboms` hook

## Files to Modify
- `src/routes.tsx` — Add route: `/sbom/compare` pointing to `SbomComparePage` (lazy-loaded, following existing route patterns)

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomDetailPage/` — main page component with a `components/` subdirectory for page-specific components.
- The `SbomComparePage` component should:
  1. Read `left` and `right` query parameters from the URL using React Router's `useSearchParams`.
  2. Render two `SbomSelector` components and a "Compare" button in the header toolbar.
  3. Use the `useSbomComparison` hook (Task 5) to fetch comparison data when both IDs are set.
  4. Render six `DiffSection` components, one for each diff category, in the order specified by the Figma design.
  5. Show `EmptyState` when no comparison has been triggered.
  6. Show `Skeleton` placeholders when the comparison query is loading.
- The `DiffSection` component should:
  1. Accept props: `title`, `badgeColor`, `count`, `isExpanded` (default: count > 0), and `children` (table content).
  2. Wrap content in PatternFly `ExpandableSection` with a `Badge` showing the item count.
  3. Render a PatternFly composable `Table` with the appropriate columns for each diff category.
- The `SbomSelector` component should:
  1. Use PatternFly `Select` with typeahead filtering.
  2. Fetch the SBOM list via the existing `useSboms` hook from `src/hooks/useSboms.ts`.
  3. Display SBOM name and version in each option.
  4. Emit the selected SBOM ID to the parent component.
- New Vulnerabilities table rows with severity "Critical" must have a highlighted background row style.
- Use existing `SeverityBadge` from `src/components/SeverityBadge.tsx` in vulnerability tables.
- Use existing `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as reference for empty state pattern (or use PatternFly `EmptyState` directly per Figma).
- Route registration in `src/routes.tsx` should follow the lazy-loading pattern used by other page routes.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity display in New/Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — empty state pattern reference
- `src/components/LoadingSpinner.tsx` — loading state reference (though Figma specifies `Skeleton` for this page)
- `src/hooks/useSboms.ts` — fetch SBOM list for selector dropdowns
- `src/hooks/useSbomComparison.ts` — React Query hook created in Task 5
- `src/utils/severityUtils.ts` — severity ordering and color mapping for vulnerability tables
- `src/pages/SbomDetailPage/` — page structure pattern reference

## Acceptance Criteria
- [ ] `SbomComparePage` renders at `/sbom/compare` route
- [ ] URL query params `left` and `right` pre-populate SBOM selectors
- [ ] Compare button triggers comparison API call via `useSbomComparison` hook
- [ ] All six diff sections render as `ExpandableSection` components with correct `Badge` colors
- [ ] Sections with >0 items default to expanded; empty sections default to collapsed
- [ ] Data tables display correct columns per the Figma design specification
- [ ] New Vulnerabilities rows with "Critical" severity have a highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Skeleton loading states display during API call
- [ ] Compare button and Export dropdown are disabled during loading
- [ ] Route is lazy-loaded following existing routing patterns

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results with correct section counts
- [ ] Unit test: expanded/collapsed state of sections matches item count
- [ ] Unit test: critical severity rows have highlighted styling
- [ ] Unit test: loading state shows skeleton placeholders

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Create React Query hook for SBOM comparison

`[sdlc-workflow] Description digest: sha256-md:f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8`
