# Task 3 — Frontend SBOM comparison page with diff sections

## Repository
trustify-ui

## Description
Build the SBOM comparison page at `/sbom/compare` based on the Figma design mockups. The page includes a header toolbar with two SBOM selector dropdowns (pre-populated from URL query params), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons by encoding both SBOM IDs in query parameters. For large diffs (>100 changed packages in any section), use virtualized lists to prevent browser freezing.

## Files to Modify
- `src/routes.tsx` — register the `/sbom/compare` route pointing to `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar component with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (wraps PatternFly `ExpandableSection` with count badge and data table)
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — table for removed packages (same columns as added)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — table for new vulnerabilities (columns: Advisory ID, Severity, Title, Affected Package); rows with severity "Critical" have highlighted background
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — table for license changes (columns: Package Name, Left License, Right License)

## Implementation Notes

### Page layout and state management
The page reads `left` and `right` query parameters from the URL on initial load. If both are present, it immediately triggers the comparison API call via `useSbomComparison` (from Task 2). If query params are absent, show the empty state. When the user selects SBOMs and clicks Compare, update the URL query params (using React Router `useSearchParams`) and let the hook react to the new IDs. This ensures URL shareability.

### Component mapping (from Figma design)
- **SBOM selectors**: PatternFly `Select` component with `variant="typeahead"` for searchable dropdown. Populate options using the existing `useSboms` hook (`src/hooks/useSboms.ts`). Display format: `"{name} {version}"`.
- **Compare button**: PatternFly `Button` with `variant="primary"`. Disabled until both selectors have values.
- **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison data is loaded. (Export is non-MVP but include the dropdown with a placeholder handler.)
- **Diff sections**: PatternFly `ExpandableSection` wrapping a `Table` (composable pattern). Each section has a title and a `Badge` showing the item count. Default expanded for sections with >0 items.
- **Count badge colors**: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow.
- **Severity display**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the severity column in vulnerability tables.
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: PatternFly `Skeleton` placeholder in each diff section while the API call is in progress. Disable the header toolbar during loading.

### Virtualization for large diffs
For diff sections with >100 rows, implement virtualized rendering to prevent browser freezing. Use `react-window` or a PatternFly-compatible virtualization approach. The virtualization threshold should be configurable but default to 100.

### Critical vulnerability highlighting
In the New Vulnerabilities table, rows where `severity` is `"critical"` must have a visually distinct background (e.g., PatternFly `--pf-v5-global--danger-color--100` or a light red background). Use the severity utilities from `src/utils/severityUtils.ts` for severity level ordering and color mapping.

### Route registration
Add the `/sbom/compare` route to `src/routes.tsx` with lazy loading, following the pattern used by existing page routes (e.g., `SbomDetailPage`, `SbomListPage`). Place it before the `/sbom/:id` route to avoid route matching conflicts.

### Data component rendering scope
All six diff section tables render data from the comparison API response at the page level (the `SbomComparisonResult`). Each table receives its corresponding array as a prop (e.g., `AddedPackagesTable` receives `data.added_packages`). The tables do not fetch data themselves.

### Relevant constraints
- Per constraints doc section 2 (Commit Rules): commits must reference TC-9003 in the footer, follow Conventional Commits format, and include the `Assisted-by: Claude Code` trailer.
- Per constraints doc section 5 (Code Change Rules): changes must be scoped to listed files; follow existing component patterns in `src/pages/`.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing hook for loading the SBOM list; use for populating the SBOM selector dropdowns
- `src/components/SeverityBadge.tsx` — existing severity display component; use in vulnerability tables
- `src/components/EmptyStateCard.tsx` — existing empty state component; reference pattern for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reference for loading state patterns
- `src/components/FilterToolbar.tsx` — existing filter toolbar; reference for toolbar layout patterns with PatternFly
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; use for critical vulnerability row highlighting
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table structure and column definition patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list; reference for advisory display patterns

## Acceptance Criteria
- [ ] `/sbom/compare` route renders the `SbomComparePage` component
- [ ] Two SBOM selector dropdowns are rendered and populated with SBOM options from the API
- [ ] Compare button is disabled when fewer than two SBOMs are selected
- [ ] Clicking Compare triggers the comparison API call and updates the URL query parameters
- [ ] Loading the page with `?left={id}&right={id}` query parameters automatically triggers the comparison
- [ ] Each of the six diff sections renders as a collapsible `ExpandableSection` with a count badge
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Count badges use the correct colors: green (added, resolved), red (removed, new vulnerabilities), blue (version changes), yellow (license changes)
- [ ] New vulnerabilities table uses `SeverityBadge` component for severity display
- [ ] Rows with critical severity in the New Vulnerabilities table have a highlighted background
- [ ] Empty state is shown when no comparison has been performed (no query params)
- [ ] Loading state (skeletons) is shown while the comparison API call is in progress
- [ ] Export dropdown is present with JSON and CSV options (placeholder handlers acceptable for MVP)
- [ ] Page handles large diffs (>100 rows per section) without browser freezing via virtualization

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders comparison results when `left` and `right` query params are provided (using MSW mock)
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: clicking Compare updates URL query parameters
- [ ] Unit test: each diff section renders correct number of rows from mock data
- [ ] Unit test: critical severity rows in New Vulnerabilities table have highlighted styling
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Tests follow Vitest + React Testing Library patterns; use MSW handlers from `tests/mocks/handlers.ts`

## Dependencies
- Depends on: Task 2 — Frontend API types, client function, and React Query hook for SBOM comparison (provides `useSbomComparison` hook and TypeScript types)
