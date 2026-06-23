## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page component at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly Select), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly ExpandableSection and Table components. The page reads SBOM IDs from URL query parameters for shareable URLs.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly ExpandableSection + Table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to SbomComparePage

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomDetailPage/SbomDetailPage.tsx` — a main page component with page-specific sub-components in a `components/` subdirectory.
- **SBOM Selectors**: Use PatternFly `Select` (single, typeahead variant) to let users pick SBOMs. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display format: "SBOM name vVersion" (e.g., "my-product-sbom v2.3.1"). Pre-populate from URL query params `left` and `right`.
- **Compare Button**: PatternFly `Button` (variant="primary"), disabled until both selectors have values. On click, update URL query params and trigger comparison via `useSbomComparison` hook.
- **Export Dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. Export converts the comparison result to the selected format and triggers a download.
- **Diff Sections**: Use `DiffSection` component wrapping PatternFly `ExpandableSection`. Each section has a title, a `Badge` with item count (colors: green for added/resolved, red for removed/new-vulns, blue for version changes, yellow for license changes), and a PatternFly `Table` (composable variant) with sortable columns. Sections default to expanded when count > 0.
- **Critical Vulnerability Highlighting**: Rows in the "New Vulnerabilities" section with severity "Critical" should have a highlighted/warning background using PatternFly modifier classes.
- **Virtualization**: For diff sections with > 100 rows, use virtualized rendering to prevent browser freezing per NFR.
- **Empty State**: When no comparison has been performed (no query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading State**: While the comparison API call is in progress, show PatternFly `Skeleton` in each diff section area. Disable the header toolbar during loading.
- **URL Shareability**: Use React Router `useSearchParams` to read and write `left` and `right` query parameters. When the page loads with both params, auto-trigger comparison.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in vulnerability diff tables.
- Route registration: add `{ path: "/sbom/compare", element: <SbomComparePage /> }` to `src/routes.tsx`, placed before the `/sbom/:id` route to avoid param conflicts.

**Figma component mapping:**
| Figma Element | PatternFly Component |
|---|---|
| SBOM selector | `Select` (single, typeahead) |
| Diff section | `ExpandableSection` |
| Count badge | `Badge` |
| Data table | `Table` (composable) |
| Severity indicator | `SeverityBadge` (existing) |
| Empty state | `EmptyState` |
| Export button | `Dropdown` |

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — existing page structure pattern with sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table rendering pattern with PatternFly Table
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability display
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern
- `src/components/FilterToolbar.tsx` — toolbar layout pattern with PatternFly
- `src/hooks/useSboms.ts` — existing hook for populating SBOM selectors
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability sections

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Both SBOM selectors populate from the SBOM list API
- [ ] Compare button triggers diff API call and displays results
- [ ] All six diff sections render with correct data and columns per Figma design
- [ ] Count badges show correct counts with appropriate colors
- [ ] Critical vulnerabilities have highlighted row background
- [ ] Empty state displays when no comparison is active
- [ ] Loading skeleton displays during API call
- [ ] URL query params `left` and `right` enable shareable comparison URLs
- [ ] Export dropdown offers JSON and CSV download options

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results with all six diff sections
- [ ] Unit test: Compare button is disabled when selectors are empty
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: Export dropdown is disabled when no comparison result is loaded
- [ ] Unit test: URL params pre-populate selectors and auto-trigger comparison

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add API types and client function for SBOM comparison

[sdlc-workflow] Description digest: sha256-md:45aabb800d40186f9ba11864f4290914912088c83740ea639501e9c2cb95c890
