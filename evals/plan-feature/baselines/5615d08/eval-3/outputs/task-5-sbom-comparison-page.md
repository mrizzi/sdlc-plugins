## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design specifications. This is the core frontend deliverable: a full-page layout with a header toolbar containing SBOM selectors and a Compare button, vertically stacked collapsible diff sections with data tables, and appropriate empty/loading states. The page reads `left` and `right` SBOM IDs from URL query parameters to support URL-shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff sections
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping a PatternFly `ExpandableSection` with a count `Badge` and a composable `Table`
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector dropdown using PatternFly `Select` (single, typeahead) that fetches the SBOM list via the existing `useSboms` hook
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — Export button using PatternFly `Dropdown` with "Export JSON" and "Export CSV" options

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to the lazy-loaded `SbomComparePage`
- `src/App.tsx` — If needed, ensure the new route is included in the router setup (follow existing pattern for other pages)

## Implementation Notes
- **Figma component mapping**: The design specifies these PatternFly 5 components:
  - **SBOM selectors**: Use PatternFly `Select` component with `variant="typeahead"` for searching. Pre-populate from URL query params `left` and `right` using `useSearchParams()` from React Router.
  - **Compare button**: PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values. On click, update URL search params and trigger the `useSbomComparison` hook.
  - **Export dropdown**: PatternFly `Dropdown` with two `DropdownItem`s: "Export JSON" and "Export CSV". Disabled until comparison data is loaded.
  - **Diff sections**: Each section uses PatternFly `ExpandableSection` with `isExpanded` defaulting to `true` when the section has items. The title includes a PatternFly `Badge` showing the count with the color specified in the Figma context: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
  - **Data tables**: Use PatternFly composable `Table` (`TableComposable`, `Thead`, `Tbody`, `Tr`, `Th`, `Td`) with sortable columns. For sections with >100 rows, implement virtualized scrolling using `react-window` or similar to prevent browser freezing (per non-functional requirements).
  - **Severity indicators**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` in the New Vulnerabilities and Resolved Vulnerabilities tables.
  - **Empty state**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."
  - **Loading state**: While the comparison API call is in flight, show PatternFly `Skeleton` placeholders in each diff section area and disable the header toolbar.
- **Critical vulnerability highlighting**: In the New Vulnerabilities table, rows where `severity` is `"critical"` should have a highlighted background (use PatternFly's `isHoverable` or a custom `className` with a warning background color).
- **URL-shareable comparisons**: Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. When the user clicks Compare, update the URL so it can be bookmarked and shared.
- **Route registration**: In `src/routes.tsx`, add a lazy-loaded route following the existing pattern for pages like `SbomListPage` and `SbomDetailPage`. Use `React.lazy(() => import('./pages/SbomComparePage/SbomComparePage'))`.
- The `SbomSelector` component should use the existing `useSboms` hook from `src/hooks/useSboms.ts` to fetch the SBOM list and display each option as "{name} {version}".
- For export functionality, serialize the `SbomComparison` data to JSON for download, and for CSV convert each diff section to rows with appropriate headers.

## Reuse Candidates
- `src/hooks/useSboms.ts` — Reuse to populate the SBOM selector dropdowns
- `src/hooks/useSbomComparison.ts` — The hook from Task 4 for fetching comparison data
- `src/components/SeverityBadge.tsx` — Reuse for severity display in vulnerability diff tables
- `src/components/EmptyStateCard.tsx` — Reference for empty state pattern, though the Figma design specifies a custom empty state
- `src/components/LoadingSpinner.tsx` — Reference for loading patterns, though Figma specifies `Skeleton` placeholders
- `src/components/FilterToolbar.tsx` — Reference for PatternFly toolbar layout patterns

## Acceptance Criteria
- [ ] Page is accessible at `/sbom/compare` route
- [ ] SBOM selectors load the list of available SBOMs and allow typeahead search
- [ ] Compare button is disabled until both SBOMs are selected
- [ ] Clicking Compare fetches the diff and renders all six diff sections
- [ ] Each diff section shows the correct count badge with the specified color (green/red/blue/yellow per Figma)
- [ ] Diff sections are expanded by default when they contain items
- [ ] Data tables display the correct columns as specified in the Figma design context
- [ ] New Vulnerabilities table uses `SeverityBadge` component and highlights critical-severity rows
- [ ] Empty state is shown when no comparison has been performed
- [ ] Loading skeletons are shown while the API call is in flight
- [ ] URL query parameters `left` and `right` are updated on Compare and pre-populate selectors on page load
- [ ] Export dropdown offers JSON and CSV options and is disabled until comparison data is loaded
- [ ] Large diffs (>100 changed packages) use virtualized lists to prevent browser freezing

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results when valid data is returned from the API
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: critical-severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: diff sections with zero items are collapsed by default

## Dependencies
- Depends on: Task 4 — Frontend API client and hook for SBOM comparison
