## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page UI based on the Figma design. The page includes a header toolbar with two SBOM selector dropdowns and a Compare button, followed by vertically stacked collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section contains a data table and a count badge. The page also provides an empty state when no comparison has been performed and skeleton loading states during API calls.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main page component orchestrating the comparison toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests with MSW mocking for the comparison page
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` -- header toolbar component with left/right SBOM selectors (PatternFly `Select` with typeahead), Compare button (PatternFly `Button` primary), and Export dropdown (PatternFly `Dropdown` secondary with JSON/CSV options)
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with a title, `Badge` count indicator, and a composable `Table` for the section's data

## Implementation Notes

### Figma Design Mapping
- **Header Toolbar**: Two PatternFly `Select` components (single-select, typeahead variant) for left/right SBOM selection. Pre-populate from URL query params `left` and `right`. Use the existing `useSboms` hook to fetch the SBOM list for the dropdowns. A primary `Button` labeled "Compare" is disabled until both selectors have values and triggers the comparison via `useSbomComparison` from Task 5. A secondary `Dropdown` labeled "Export" with menu items "Export JSON" and "Export CSV" is disabled until comparison data is loaded.
- **Diff Sections**: Six PatternFly `ExpandableSection` components, each containing a composable `Table`. Sections with >0 items are expanded by default. Each section title includes a `Badge` with the item count: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
- **Added Packages table**: columns -- Package Name, Version, License, Advisories (count).
- **Removed Packages table**: columns -- Package Name, Version, License, Advisories (count).
- **Version Changes table**: columns -- Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
- **New Vulnerabilities table**: columns -- Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" have a highlighted background (use PatternFly `isRowSelected` or custom CSS class).
- **Resolved Vulnerabilities table**: columns -- Advisory ID, Severity, Title, Previously Affected Package.
- **License Changes table**: columns -- Package Name, Left License, Right License.
- **Empty State**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading State**: PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress. The header toolbar is disabled during loading.
- **Virtualization**: For diff sections with >100 rows, use virtualized rendering to prevent browser freezing with large diffs.

### Patterns and Reuse
- Follow the page component structure in `src/pages/SbomDetailPage/SbomDetailPage.tsx` with a main page component and `components/` subdirectory for page-specific components.
- Reuse the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity indicators in the vulnerability tables.
- Reuse the existing `EmptyStateCard` component pattern from `src/components/EmptyStateCard.tsx` for the initial empty state.
- Reuse the existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` as a fallback alongside Skeleton placeholders.
- URL state: read `left` and `right` from URL search params using React Router's `useSearchParams()`. Update the URL when the user clicks Compare so the comparison is URL-shareable and bookmarkable.
- Per CONVENTIONS.md §Component naming: use PascalCase for all component file names. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.
- Per CONVENTIONS.md §MSW mocking: use MSW request handlers for API mocking in tests. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.ts` test file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx::SeverityBadge` -- severity level badge for vulnerability tables; reuse directly
- `src/components/EmptyStateCard.tsx::EmptyStateCard` -- empty state placeholder pattern; follow for the "no comparison yet" state
- `src/components/LoadingSpinner.tsx::LoadingSpinner` -- loading indicator; use as fallback during comparison loading
- `src/hooks/useSboms.ts::useSboms` -- fetches SBOM list for the selector dropdowns
- `src/hooks/useSbomComparison.ts::useSbomComparison` -- created in Task 5; provides comparison data, loading, and error states
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- follow page structure pattern with components/ subdirectory
- `src/utils/severityUtils.ts` -- severity ordering and color mapping; reuse for critical-row highlighting logic

## Acceptance Criteria
- [ ] Comparison page renders header toolbar with left/right SBOM selectors, Compare button, and Export dropdown per Figma design
- [ ] Selecting two SBOMs and clicking Compare fetches and displays the structured diff
- [ ] Six diff sections render with correct PatternFly `ExpandableSection`, `Badge` counts, and `Table` columns matching the Figma specification
- [ ] New Vulnerabilities rows with severity "Critical" have highlighted background
- [ ] Empty state displays PatternFly `EmptyState` with `CodeBranchIcon` when no comparison is loaded
- [ ] Skeleton loading states appear during API call
- [ ] URL updates with `left` and `right` query params when comparison is performed
- [ ] Page loads comparison directly when opened with `left` and `right` query params (URL-shareable)
- [ ] Diff sections with >100 rows use virtualized rendering

## Test Requirements
- [ ] Test: page renders empty state when no query params are present
- [ ] Test: selecting two SBOMs and clicking Compare triggers API call and renders diff sections
- [ ] Test: diff sections show correct count badges and table data from mock response
- [ ] Test: New Vulnerabilities section highlights critical-severity rows
- [ ] Test: Export dropdown is disabled until comparison data is loaded

## Verification Commands
- `npx tsc --noEmit` -- no TypeScript compilation errors
- `npx vitest run src/pages/SbomComparePage` -- comparison page unit tests pass

## Dependencies
- Depends on: Task 2 -- Create feature branch (trustify-ui)
- Depends on: Task 5 -- Add API types, client function, and React Query hook for SBOM comparison

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
