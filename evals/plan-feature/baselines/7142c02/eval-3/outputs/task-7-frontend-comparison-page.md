## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page UI following the Figma design. This page displays a header toolbar with SBOM selectors and a "Compare" button, followed by vertically stacked collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section contains a data table with appropriate columns and count badges. The page supports URL-shareable comparisons via query parameters.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and data `Table`
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar with SBOM selectors, Compare button, and Export dropdown
- `src/pages/SbomComparePage/components/CompareEmptyState.tsx` — Empty state shown when no comparison has been performed

## Implementation Notes
**Figma Design Reference (from figma-context.md):**

### Header Toolbar (CompareToolbar)
- **Left SBOM selector**: PatternFly `Select` (single, typeahead) showing SBOM name and version (e.g., "my-product-sbom v2.3.1"). Pre-populated from URL query param `left`. Fetch SBOM list via existing `useSboms` hook.
- **Right SBOM selector**: Identical `Select` dropdown for the second SBOM. Pre-populated from URL query param `right`.
- **"Compare" button**: PatternFly primary `Button`, disabled until both selectors have values. Triggers the diff API call by updating URL query params.
- **"Export" dropdown**: PatternFly `Dropdown` (secondary) with "Export JSON" and "Export CSV" items. Disabled until a comparison result is loaded.

### Diff Sections (DiffSection)
Each section is a PatternFly `ExpandableSection` with:
- Title and count `Badge` (color varies: green for added/resolved, red for removed/new vulns, blue for version changes, yellow for license changes)
- PatternFly composable `Table` inside with sortable columns
- Default expanded for sections with >0 items

Section order and columns per Figma:
1. **Added Packages** — Package Name, Version, License, Advisories (count). Badge: green.
2. **Removed Packages** — Package Name, Version, License, Advisories (count). Badge: red.
3. **Version Changes** — Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Badge: blue.
4. **New Vulnerabilities** — Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Badge: red. Rows with severity "Critical" have a highlighted background.
5. **Resolved Vulnerabilities** — Advisory ID, Severity, Title, Previously Affected Package. Badge: green.
6. **License Changes** — Package Name, Left License, Right License. Badge: yellow.

### Empty State (CompareEmptyState)
Per Figma: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

### Loading State
Per Figma: PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress. Header toolbar is disabled during loading.

### URL Shareability
- Read `left` and `right` query params from the URL on page load using React Router's `useSearchParams`.
- When both are present, auto-trigger the comparison.
- When the user clicks "Compare", update the URL query params so the comparison is bookmarkable.

### Virtualization
- For diff sections with >100 rows, use virtualized lists to prevent browser freezing per non-functional requirements.

- Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/SbomComparePage/` directory matching the convention's page directory scope.
- Per CONVENTIONS.md §Naming: PascalCase for components. Applies: task creates `SbomComparePage.tsx`, `DiffSection.tsx`, `CompareToolbar.tsx`, `CompareEmptyState.tsx` matching the convention's component naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.test.tsx` file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Existing severity badge component for the New/Resolved Vulnerabilities sections
- `src/components/EmptyStateCard.tsx` — Pattern for empty state (though the comparison page uses a custom empty state per Figma)
- `src/components/LoadingSpinner.tsx` — Loading indicator pattern reference
- `src/components/FilterToolbar.tsx` — PatternFly toolbar pattern reference for the CompareToolbar
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Table component pattern for package data tables
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Advisory list pattern for vulnerability sections
- `src/hooks/useSboms.ts` — Used to populate the SBOM selector dropdowns

## Acceptance Criteria
- [ ] Comparison page renders with header toolbar containing two SBOM selectors and Compare button
- [ ] SBOM selectors are PatternFly `Select` (single, typeahead) populated from the SBOM list API
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API and renders six diff sections
- [ ] Each diff section is a PatternFly `ExpandableSection` with correct title, count badge (with correct color), and data table
- [ ] New Vulnerabilities section highlights Critical severity rows with a distinct background
- [ ] Severity values use the existing `SeverityBadge` component
- [ ] Empty state displays when no comparison has been performed (per Figma: CodeBranchIcon, correct title and body text)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL query params `left` and `right` are read on page load and auto-trigger comparison
- [ ] URL is updated when Compare is clicked, making the comparison shareable/bookmarkable
- [ ] Diff sections with >100 rows use virtualized rendering

## Test Requirements
- [ ] Unit test: renders empty state when no SBOM IDs are provided
- [ ] Unit test: renders toolbar with two selectors and a disabled Compare button
- [ ] Unit test: Compare button becomes enabled when both selectors have values
- [ ] Unit test: renders all six diff sections with correct data after comparison
- [ ] Unit test: DiffSection component renders ExpandableSection with correct badge color and count
- [ ] Unit test: Critical severity rows in New Vulnerabilities have highlighted background
- [ ] Unit test: reads `left` and `right` from URL search params and auto-triggers comparison

## Dependencies
- Depends on: Task 6 — Add API types, client function, and React Query hook for SBOM comparison

[sdlc-workflow] Description digest: sha256-md:a60bfab0fccd79242890416ee6777c094e6c891298af7c31d6f731215b7b82d4
