## Repository
trustify-ui

## Target Branch
main

## Description
Build the SBOM comparison page UI at `/sbom/compare` based on the Figma design. The page includes SBOM selector dropdowns, a Compare button, six collapsible diff sections with data tables, empty/loading states, and URL-shareable comparison via query parameters. This is the primary user-facing deliverable for the SBOM comparison feature.

## Files to Create
- `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` -- Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` -- Unit tests for the comparison page
- `src/pages/SbomComparisonPage/components/DiffSection.tsx` -- Reusable collapsible diff section wrapping PatternFly `ExpandableSection` with count `Badge` and `Table`
- `src/pages/SbomComparisonPage/components/SbomSelector.tsx` -- SBOM selector dropdown using PatternFly `Select` with typeahead, backed by `useSboms` hook

## Files to Modify
- `src/routes.tsx` -- Add route for `/sbom/compare` pointing to the new `SbomComparisonPage` component (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` -- Add checkbox selection for SBOMs and a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
### Page layout and routing
- Register the route in `src/routes.tsx` following the existing lazy-loading pattern (e.g., `React.lazy(() => import(...))`).
- Read `left` and `right` query params from the URL using React Router's `useSearchParams`. When the user clicks Compare, update the URL search params so the comparison is URL-shareable (UC-2).

### Header toolbar (Figma: Header Toolbar)
- Use two `SbomSelector` components side by side. Each is a PatternFly `Select` with `variant="typeahead"` that fetches the SBOM list via the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in each option.
- "Compare" button: PatternFly `Button` with `variant="primary"`, disabled until both selectors have values. On click, update URL search params and trigger the `useSbomComparison` hook (from Task 3).
- "Export" dropdown: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV"). Disabled until comparison data is loaded. This is non-MVP but include the UI skeleton with disabled state for now.

### Diff sections (Figma: Diff Sections)
- Create a reusable `DiffSection` component that accepts: `title`, `items[]`, `columns[]`, `badgeColor`, `defaultExpanded`.
- Each `DiffSection` renders a PatternFly `ExpandableSection` with the title and a PatternFly `Badge` showing the item count. Inside, render a PatternFly composable `Table` with sortable columns.
- Sections and their badge colors:
  1. Added Packages -- green badge. Columns: Package Name, Version, License, Advisories (count).
  2. Removed Packages -- red badge. Columns: Package Name, Version, License, Advisories (count).
  3. Version Changes -- blue badge. Columns: Package Name, Left Version, Right Version, Direction.
  4. New Vulnerabilities -- red badge. Columns: Advisory ID, Severity (render with existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" should have a highlighted background row style.
  5. Resolved Vulnerabilities -- green badge. Columns: Advisory ID, Severity, Title, Previously Affected Package.
  6. License Changes -- yellow badge. Columns: Package Name, Left License, Right License.
- Default expanded: sections with >0 items are expanded by default; empty sections are collapsed.
- For large diffs (>100 rows), use virtualized rendering to prevent browser freezing per the non-functional requirements.

### Empty state (Figma: Empty State)
- When no comparison has been performed (no query params or selectors not filled), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."

### Loading state (Figma: Loading State)
- While `useSbomComparison` is loading, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.

### SBOM list page integration
- In `src/pages/SbomListPage/SbomListPage.tsx`, add a checkbox column to the existing SBOM table. When exactly two SBOMs are checked, enable a "Compare selected" button (PatternFly `Button`, `variant="secondary"`) that navigates to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.

## Reuse Candidates
- `src/hooks/useSboms.ts` -- Fetch SBOM list for the selector dropdowns
- `src/hooks/useSbomComparison.ts` -- React Query hook from Task 3 for fetching comparison data
- `src/components/SeverityBadge.tsx` -- Render severity indicators in the New Vulnerabilities and Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` -- Pattern reference for empty state layout (adapt with custom icon and text)
- `src/components/LoadingSpinner.tsx` -- Pattern reference for loading states (use PatternFly `Skeleton` instead for this page)
- `src/components/FilterToolbar.tsx` -- Pattern reference for toolbar layout conventions
- `src/utils/severityUtils.ts` -- Severity color mapping for critical row highlighting

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and renders the comparison page
- [ ] SBOM selector dropdowns load and display available SBOMs with name and version
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare updates the URL with `left` and `right` query params
- [ ] Loading the page with `left` and `right` query params auto-populates selectors and triggers comparison
- [ ] All six diff sections render with correct data, column headers, and badge colors
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state displays when no comparison is active
- [ ] Loading skeletons display while comparison is in progress
- [ ] SbomListPage has checkbox selection and "Compare selected" button for exactly two selected SBOMs
- [ ] Existing `SeverityBadge` component is used for severity columns (no new severity rendering)

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params
- [ ] Unit test: comparison page renders diff sections when comparison data is provided (mock via MSW)
- [ ] Unit test: Compare button is disabled when only one selector has a value
- [ ] Unit test: URL query params are updated when Compare is clicked
- [ ] Unit test: Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: SbomListPage "Compare selected" button appears only when exactly two SBOMs are checked
- [ ] Unit test: DiffSection component expands by default when items > 0 and collapses when items = 0

## Verification Commands
- `npx vitest run src/pages/SbomComparisonPage` -- Comparison page tests pass
- `npx tsc --noEmit` -- No TypeScript compilation errors
- `npx vite build` -- Production build succeeds

## Dependencies
- Depends on: Task 3 -- Frontend API layer and hook (provides `useSbomComparison` hook and TypeScript types)
