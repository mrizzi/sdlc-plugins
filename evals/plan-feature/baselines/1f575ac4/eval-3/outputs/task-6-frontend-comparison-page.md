## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the SBOM comparison page component at `/sbom/compare` with the full UI as specified in the Figma design: header toolbar with SBOM selectors and Compare button, six collapsible diff sections with data tables, empty state, and loading state. This is the primary user-facing component for the SBOM comparison feature.

## Files to Modify
- `src/routes.tsx` — add `/sbom/compare` route pointing to the new comparison page

## Files to Create
- `src/pages/SbomComparisonPage/SbomComparisonPage.tsx` — main comparison page component
- `src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparisonPage/components/DiffSection.tsx` — reusable diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparisonPage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## Implementation Notes
- Follow the existing page structure pattern from `src/pages/SbomDetailPage/SbomDetailPage.tsx` — each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory.
- **Header Toolbar**: Use PatternFly `Select` (single, typeahead) for both SBOM selector dropdowns. Populate them using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version in dropdown items. Pre-populate selectors from URL query params `left` and `right`.
- **Compare button**: PatternFly primary `Button`, disabled until both selectors have values. On click, update URL query params and trigger the `useSbomComparison` hook.
- **Export dropdown**: PatternFly `Dropdown` with "Export JSON" and "Export CSV" items. Disabled until comparison data is loaded. Export is a non-MVP feature — implement the dropdown UI but the actual export logic can be a follow-up.
- **URL-shareable comparison**: Use React Router's `useSearchParams` to read/write `left` and `right` query params. When both params are present on page load, auto-trigger the comparison.
- **Diff sections**: Create a reusable `DiffSection` component using PatternFly `ExpandableSection`. Each section has:
  - Title with count `Badge` (color varies: green for added/resolved, red for removed/new vulnerabilities, blue for version changes, yellow for license changes)
  - PatternFly `Table` (composable) with sortable columns
  - Default expanded when section has >0 items
- **Section order**: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes.
- **New Vulnerabilities section**: Rows with severity "Critical" must have a highlighted background. Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display.
- **Empty state**: When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as a reference.
- **Loading state**: While the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading.
- **Virtualized lists**: For sections with >100 rows, use virtualized rendering to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support.
- **Route registration**: Add the route in `src/routes.tsx` following the pattern of existing routes. Use lazy loading for the page component.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity display in the New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern
- `src/components/LoadingSpinner.tsx` — loading indicator during API calls
- `src/components/FilterToolbar.tsx` — reference for toolbar layout patterns with PatternFly
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for package table column definitions and rendering
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory display patterns
- `src/hooks/useSboms.ts` — powers SBOM selector dropdowns
- `src/utils/severityUtils.ts` — severity ordering and color mapping for vulnerability diff display
- `src/routes.tsx` — route registration pattern

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] SBOM selector dropdowns load and display available SBOMs
- [ ] Compare button triggers comparison when both SBOMs are selected
- [ ] All six diff sections render with correct data, count badges, and badge colors
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Critical vulnerability rows have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading state displays skeleton placeholders during API call
- [ ] URL query params encode both SBOM IDs for bookmarking and sharing
- [ ] Page loads comparison directly when URL contains both `left` and `right` params

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no query params are present
- [ ] Unit test: comparison page renders diff sections when comparison data is returned
- [ ] Unit test: verify correct badge colors for each diff section
- [ ] Unit test: verify critical vulnerability rows are highlighted
- [ ] Unit test: verify Compare button is disabled when selectors are empty
- [ ] Unit test: verify URL params update when comparison is triggered

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 5 — Frontend API layer (models, rest function, hook)
