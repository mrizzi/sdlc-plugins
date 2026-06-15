# Task 6 — Build SBOM comparison page UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page component following the Figma design. The page provides a header toolbar with two SBOM selectors and a Compare button, followed by collapsible diff sections showing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The page reads SBOM IDs from URL query parameters for shareability and uses virtualized lists for large diffs (>100 items).

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors and action buttons
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table for added/removed packages and version changes
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table for new/resolved vulnerabilities
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table for license changes

## Implementation Notes
**Figma design reference** — The UI follows the Figma mockup for the SBOM Comparison View (SBOMCompare mock123, Comparison View page).

### ComparisonToolbar.tsx
- Two PatternFly `Select` components (single-select, typeahead variant) for choosing left and right SBOMs. Each selector shows SBOM name and version (e.g., "my-product-sbom v2.3.1"). Use the existing `useSboms` hook to populate options.
- Pre-populate selectors from URL query params `left` and `right` via `useSearchParams`.
- PatternFly primary `Button` labeled "Compare" -- disabled until both selectors have values. On click, update URL query params and trigger the comparison via `useSbomComparison`.
- PatternFly `Dropdown` labeled "Export" with items "Export JSON" and "Export CSV". Disabled until comparison data is loaded. (Export is non-MVP, wire up UI only with placeholder handlers.)
- Toolbar is disabled during loading state.

### DiffSection.tsx
- Wraps a PatternFly `ExpandableSection` component.
- Props: `title: string`, `count: number`, `badgeColor: string`, `isLoading: boolean`, `children: ReactNode`.
- Title includes a PatternFly `Badge` with the item count. Badge color varies by section: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes (per Figma spec).
- Default expanded when count > 0, collapsed when count is 0.
- Shows PatternFly `Skeleton` placeholder during loading state.

### PackageDiffTable.tsx
- Used for Added Packages, Removed Packages, and Version Changes sections.
- PatternFly composable `Table` with sortable columns.
- Added/Removed columns: Package Name, Version, License, Advisories (count).
- Version Changes columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
- Use virtualized rendering for >100 rows to meet the non-functional requirement of handling large diffs without browser freezing.

### VulnerabilityDiffTable.tsx
- Used for New Vulnerabilities and Resolved Vulnerabilities sections.
- PatternFly composable `Table` with sortable columns.
- New Vulnerabilities columns: Advisory ID, Severity (rendered with existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package.
- Resolved Vulnerabilities columns: Advisory ID, Severity, Title, Previously Affected Package.
- Rows with severity "Critical" have a highlighted background (per Figma spec) -- use PatternFly `isHoverable` row styling or custom CSS with `--pf-v5-global--danger-color--100`.

### LicenseChangeTable.tsx
- PatternFly composable `Table` with columns: Package Name, Left License, Right License.

### SbomComparePage.tsx
- Reads `left` and `right` from URL search params using `useSearchParams`.
- Calls `useSbomComparison(leftId, rightId)` to fetch comparison data.
- Renders `ComparisonToolbar` at the top.
- When no comparison is loaded (no query params), renders PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." (per Figma spec).
- When data is loaded, renders six `DiffSection` components in order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- URL is updated with both SBOM IDs for bookmarkability/shareability.

### Existing components to reuse
- `src/components/SeverityBadge.tsx` — for vulnerability severity indicators
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern (but use PatternFly `EmptyState` directly per Figma)
- `src/components/LoadingSpinner.tsx` — reference for loading patterns
- `src/hooks/useSboms.ts` — for populating SBOM selector dropdowns

Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
Applies: task creates PatternFly-based components in `src/pages/SbomComparePage/` matching the convention's component library scope.

Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/` directory matching the convention's page structure scope.

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task creates `SbomComparePage.test.tsx` matching the convention's testing scope.

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with PatternFly layout
- [ ] Two SBOM Select dropdowns (typeahead) populated via `useSboms` hook
- [ ] Compare button disabled until both SBOMs selected; triggers comparison on click
- [ ] URL updates with `?left={id}&right={id}` for shareability
- [ ] Page loads comparison directly when URL contains both query params
- [ ] Six diff sections render as PatternFly ExpandableSection with correct Badge colors (green/red/blue/yellow per Figma)
- [ ] ExpandableSection defaults to expanded when section has items, collapsed when empty
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] SeverityBadge component used for vulnerability severity display
- [ ] EmptyState shown on initial load with CodeBranchIcon, "Select two SBOMs to compare" title
- [ ] Skeleton placeholders shown during API loading
- [ ] Tables support sorting and are virtualized for >100 rows
- [ ] Export dropdown is present with JSON/CSV options (disabled until data loaded)

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders comparison results when data is loaded (mock via MSW)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: URL updates when comparison is triggered
- [ ] Unit test: Critical severity rows are visually highlighted in the New Vulnerabilities section
- [ ] Unit test: all six diff sections render with correct titles and badge counts

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 5 — Add SBOM comparison hook and route

[sdlc-workflow] Description digest: sha256-md:71e65d36f60e3c9f4b9e48a0cee39e159bf8484e2019ec87933cd897be0e4103
