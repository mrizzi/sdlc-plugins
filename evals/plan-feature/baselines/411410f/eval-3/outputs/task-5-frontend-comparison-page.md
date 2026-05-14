# Task 5: Build the SBOM comparison page UI

## Repository
trustify-ui

## Target Branch
main

## Description
Implement the main SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors and a Compare button, six collapsible diff sections with data tables, empty state and loading state handling, and URL-based state for shareability. This is the core user-facing deliverable for the feature.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — PatternFly `Select` (single, typeahead) component for choosing an SBOM. Uses the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with a `Badge` count and a `Table` inside
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — PatternFly `Dropdown` component with "Export JSON" and "Export CSV" items

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded `SbomComparePage`

## Implementation Notes
- **Page structure** (`SbomComparePage.tsx`):
  - Use React Router `useSearchParams` to read `left` and `right` query parameters from the URL, enabling shareable comparison URLs.
  - **Header toolbar**: Render two `SbomSelector` components side by side and a primary "Compare" button. The Compare button should be disabled until both selectors have values. When clicked, update the URL search params and trigger the comparison via `useSbomComparison` hook from `src/hooks/useSbomComparison.ts`.
  - **Diff sections**: Render six `DiffSection` components in the order specified by the Figma design: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
  - **Empty state**: When no comparison has been performed (no query params), render a PatternFly `EmptyState` component with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed." Reference the existing `EmptyStateCard` pattern in `src/components/EmptyStateCard.tsx`.
  - **Loading state**: While `useSbomComparison` is loading, render PatternFly `Skeleton` placeholders inside each diff section. Disable the header toolbar during loading.

- **SbomSelector** (`components/SbomSelector.tsx`):
  - Use PatternFly `Select` with `variant="typeahead"` for searchable SBOM selection.
  - Fetch the SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`.
  - Display SBOM name and version in each option (e.g., "my-product-sbom v2.3.1").
  - Accept an `onChange(sbomId: string)` callback prop and a `selectedId` prop for controlled behavior.
  - Pre-populate selection from URL query param.

- **DiffSection** (`components/DiffSection.tsx`):
  - Wrap PatternFly `ExpandableSection` with a title and a PatternFly `Badge` showing the item count.
  - Badge colors by section per Figma: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow (gold) for License Changes.
  - Default expanded when count > 0, collapsed when count === 0.
  - Render a PatternFly composable `Table` inside the section with sortable columns.
  - For the New Vulnerabilities table, use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` to render the severity column. Rows with severity "Critical" should have a highlighted/warning background row style.
  - Use `src/utils/severityUtils.ts` for severity ordering and color mapping.

- **ExportDropdown** (`components/ExportDropdown.tsx`):
  - PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV".
  - Disabled when no comparison data is loaded.
  - Export JSON: serialize the `SbomComparison` data to a JSON file download.
  - Export CSV: convert the diff data to CSV format and trigger a file download.
  - Note: Export is not MVP per the feature spec; implement a basic version and mark with a TODO for enhancement.

- **Route registration** in `src/routes.tsx`:
  - Follow the existing pattern of lazy-loaded routes (e.g., `SbomDetailPage`).
  - Path: `/sbom/compare` — place this BEFORE the `/sbom/:id` route to avoid the parameterized route matching "compare" as an ID.

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and empty state
- [ ] Both SBOM selectors load the SBOM list and allow typeahead search
- [ ] Compare button triggers the API call and renders diff sections with data
- [ ] All six diff sections render with correct PatternFly `ExpandableSection`, `Badge` (with correct colors), and `Table` components
- [ ] New Vulnerabilities section uses `SeverityBadge` component and highlights Critical rows
- [ ] Empty state displays when no query params are present, with `CodeBranchIcon` and correct text
- [ ] Loading state shows `Skeleton` placeholders during API call
- [ ] URL includes `left` and `right` query params after comparison — page can be refreshed or shared
- [ ] Export dropdown renders with JSON and CSV options

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results when query params are provided and API returns data
- [ ] Unit test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Unit test: diff sections are expanded by default when they contain items, collapsed when empty

## Dependencies
- Depends on: Task 4 — Add frontend API client and React Query hook for SBOM comparison
