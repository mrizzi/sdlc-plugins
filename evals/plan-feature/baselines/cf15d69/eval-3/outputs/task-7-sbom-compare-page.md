## Repository
trustify-ui

## Target Branch
main

## Description
Create the SBOM comparison page component at `/sbom/compare`. This is the core UI for the feature: a full-page layout with SBOM selector dropdowns, a Compare button, and six collapsible diff sections showing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The page reads `left` and `right` SBOM IDs from URL query parameters to support URL-shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component with count badge and data table
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
**Page structure** (per Figma design context):

The page is a full-page layout with a header toolbar and vertically stacked collapsible diff sections.

**CompareToolbar component:**
- Two PatternFly `Select` components (single, typeahead) for left and right SBOM selection. Pre-populate from URL query params `left` and `right`. Fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in the dropdown options (e.g., "my-product-sbom v2.3.1").
- A primary PatternFly `Button` labeled "Compare", disabled until both selectors have values. On click, update URL query params and trigger the comparison query.
- A secondary PatternFly `Dropdown` labeled "Export" with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. Export triggers a client-side download of the comparison result data.

**DiffSection component:**
- Wraps a PatternFly `ExpandableSection` with a title, a PatternFly `Badge` showing the item count, and a PatternFly `Table` (composable) inside. Default expanded when item count > 0.
- Badge color varies by section: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- Table columns are specific to each diff category (see Figma design context for column definitions).
- For the New Vulnerabilities section, rows with severity "Critical" should have a highlighted background row style.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity indicators in vulnerability tables.

**SbomComparePage component:**
- Read `left` and `right` from URL search params using `useSearchParams` from React Router.
- Call `useSbomComparison(left, right)` to get the comparison data.
- When no comparison has been performed (no query params), show a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` pattern from `src/components/EmptyStateCard.tsx` as reference.
- During loading, show PatternFly `Skeleton` placeholders in each diff section area. Disable the toolbar during loading.
- Render six `DiffSection` instances in order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- For tables with >100 rows, implement virtualized rendering to prevent browser freezing (per non-functional requirements).

Per Key Conventions (Page structure): Each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` and `src/pages/SbomComparePage/components/` matching the convention's page structure scope.

Per Key Conventions (Component library): All UI components use PatternFly 5. Applies: task creates page and sub-components using PatternFly `Select`, `Badge`, `ExpandableSection`, `Table`, `EmptyState`, `Button`, `Dropdown`, `Skeleton` components matching the convention's component library scope.

Per Key Conventions (Naming): PascalCase for components. Applies: task creates `SbomComparePage.tsx`, `DiffSection.tsx`, `CompareToolbar.tsx` matching the convention's naming scope.

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar and six diff sections
- [ ] SBOM selectors load SBOM list from existing `useSboms` hook
- [ ] Compare button triggers comparison API call and updates URL params
- [ ] URL query params `left` and `right` are read on page load for shareable URLs
- [ ] Empty state displays when no comparison is loaded
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] Each diff section shows correct count badge with appropriate color
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Existing `SeverityBadge` component is reused for vulnerability severity
- [ ] Export dropdown offers JSON and CSV download options

## Test Requirements
- [ ] Unit test: CompareToolbar renders two Select dropdowns and a Compare button
- [ ] Unit test: DiffSection renders ExpandableSection with correct badge count and color
- [ ] Unit test: SbomComparePage shows empty state when no query params
- [ ] Unit test: SbomComparePage renders diff sections when comparison data is present

## Dependencies
- Depends on: Task 5 — Frontend API types and client function
- Depends on: Task 6 — Frontend comparison hook

[sdlc-workflow] Description digest: sha256-md:1765ddcee9284312c2eead87296d44c23f05ea9d5fa2d28ec299b0716c89d5d7
