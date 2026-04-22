## Repository
trustify-ui

## Description
Build the SBOM comparison page UI at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly `Select`), a Compare button, an Export dropdown, and vertically stacked collapsible diff sections (PatternFly `ExpandableSection`) each containing a data table. The page reads `left` and `right` query params from the URL to support shareable links.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component orchestrating toolbar and diff sections
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with two PatternFly `Select` dropdowns (typeahead, single-select), a primary "Compare" button, and a secondary "Export" `Dropdown` with JSON and CSV options
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section using PatternFly `ExpandableSection` with a `Badge` count and a composable `Table` inside
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page

## Files to Modify
- `src/routes.tsx` — Add route entry: `{ path: "/sbom/compare", element: <SbomComparePage /> }` with lazy loading

## Implementation Notes
- **CompareToolbar.tsx**: Use PatternFly `Select` component with `variant="typeahead"` for each SBOM selector. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option label. The "Compare" button should be a PatternFly `Button` with `variant="primary"`, disabled until both selectors have values. The "Export" button should be a PatternFly `Dropdown` with `variant="secondary"` containing two items: "Export JSON" and "Export CSV".
- **DiffSection.tsx**: Each section wraps a PatternFly `ExpandableSection`. The title prop includes the section name and a PatternFly `Badge` showing the count of items, with badge color varying by section: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes. Sections with >0 items should default to expanded. Inside each section, render a PatternFly composable `Table` with sortable columns. For tables with >100 rows, use a virtualized list to avoid browser freezing (per NFR).
- **SbomComparePage.tsx**: Read `left` and `right` from URL query params using React Router's `useSearchParams()`. If both are present on mount, auto-trigger comparison. Pass IDs to `useSbomComparison` hook from `src/hooks/useSbomComparison.ts`. When no comparison is loaded, show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." During loading, show PatternFly `Skeleton` placeholders in each diff section area and disable the toolbar.
- **Diff sections order** (per Figma): Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- **New Vulnerabilities section**: Rows with severity "Critical" should have a highlighted background row style. Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the severity column.
- **Route registration**: Follow the lazy-loading pattern used by other pages in `src/routes.tsx`.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing shared component for severity display in New/Resolved Vulnerabilities tables
- `src/components/EmptyStateCard.tsx` — Reference for empty state pattern (though this page uses PatternFly `EmptyState` directly per Figma)
- `src/components/LoadingSpinner.tsx` — Reference for loading pattern (this page uses `Skeleton` per Figma)
- `src/hooks/useSboms.ts` — Existing hook for fetching SBOM list to populate selectors
- `src/hooks/useSbomComparison.ts` — Hook created in Task 4 for fetching comparison data
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Pattern reference for rendering package data in a table
- `src/utils/severityUtils.ts` — Severity ordering and color mapping for vulnerability tables

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selectors populated from existing SBOM list via `useSboms` hook
- [ ] "Compare" button triggers API call and renders structured diff in six collapsible sections
- [ ] URL query params `left` and `right` are updated when comparison is performed
- [ ] Page loads comparison directly when accessed with both query params (URL-shareable)
- [ ] Empty state shown when no comparison is active
- [ ] Loading skeletons shown while comparison API call is in progress
- [ ] Critical vulnerabilities are visually highlighted in the New Vulnerabilities section
- [ ] Tables use virtualized rendering for >100 rows
- [ ] Export dropdown offers JSON and CSV options

## Test Requirements
- [ ] Test that empty state renders when no query params are present
- [ ] Test that comparison results render correctly when mock data is returned
- [ ] Test that SBOM selectors populate from mock SBOM list data
- [ ] Test that URL updates with selected SBOM IDs after comparison

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run src/pages/SbomComparePage` — component tests pass

## Dependencies
- Depends on: Task 4 — Frontend API layer and comparison hook
