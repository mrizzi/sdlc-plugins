## Repository
trustify-ui

## Target Branch
main

## Description
Create the SBOM comparison page at `/sbom/compare` with a full PatternFly-based UI for viewing structured diffs between two SBOMs. The page includes a header toolbar with SBOM selectors (PatternFly `Select`), a Compare button, and an Export dropdown (PatternFly `Dropdown`), followed by six collapsible diff sections (PatternFly `ExpandableSection`) each containing a data table (PatternFly `Table`). The page supports URL-shareable comparisons via query parameters (`?left={id1}&right={id2}`) and handles empty state (PatternFly `EmptyState`) and loading state (PatternFly `Skeleton`) per the Figma design.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests for the comparison page component
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- reusable collapsible diff section component wrapping PatternFly `ExpandableSection` with count `Badge` and composable `Table`
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` -- header toolbar component with SBOM `Select` dropdowns, Compare `Button`, and Export `Dropdown`

## Files to Modify
- `src/routes.tsx` -- add route `/sbom/compare` mapped to `SbomComparePage` (lazy-loaded)

## Implementation Notes
**Figma design reference (from figma-context.md):**

**Header Toolbar (CompareToolbar component):**
- Left and right SBOM selectors: PatternFly `Select` (single, typeahead). Pre-populate from URL query params `left` and `right`. Fetch SBOM list via existing `useSboms` hook from `src/hooks/useSboms.ts`.
- Compare button: PatternFly primary action `Button`, disabled until both selectors have values.
- Export dropdown: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. (Note: Export functionality is non-MVP per the feature requirements; the dropdown renders but export logic is deferred to a follow-up task.)

**Diff Sections (DiffSection reusable component, each using PatternFly `ExpandableSection`):**
1. **Added Packages** -- table columns: Package Name, Version, License, Advisories (count). Count `Badge` color: green. Default expanded when count > 0.
2. **Removed Packages** -- same columns as Added. Count `Badge` color: red.
3. **Version Changes** -- table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade). Count `Badge` color: blue.
4. **New Vulnerabilities** -- table columns: Advisory ID, Severity (using existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`), Title, Affected Package. Count `Badge` color: red. Rows with severity "Critical" must have a highlighted background.
5. **Resolved Vulnerabilities** -- table columns: Advisory ID, Severity, Title, Previously Affected Package. Count `Badge` color: green.
6. **License Changes** -- table columns: Package Name, Left License, Right License. Count `Badge` color: yellow.

**Data tables:** Use PatternFly `Table` (composable) with sortable columns. For sections with >100 rows, implement virtualized rendering to prevent browser freezing (per non-functional requirements).

**Empty State:** When no comparison has been performed (page load without query params), show PatternFly `EmptyState` with `CodeBranchIcon` (PatternFly icon), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."

**Loading State:** While API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Header toolbar is disabled during loading.

**URL sharing:** Read `left` and `right` from URL search params on mount using React Router's `useSearchParams`. When Compare is clicked, update URL search params so the comparison is bookmarkable and shareable.

Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Component Library: PatternFly 5 -- all UI components use PF5 equivalents.
Applies: task creates `src/pages/SbomComparePage/components/DiffSection.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Naming: PascalCase for components, kebab-case for directories.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- existing shared component for severity level badges; reuse in New/Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` -- existing empty state placeholder; reference for the comparison empty state layout
- `src/components/LoadingSpinner.tsx` -- existing loading indicator; may complement Skeleton placeholders
- `src/components/FilterToolbar.tsx` -- existing filter toolbar component; reference for toolbar layout patterns with PatternFly
- `src/hooks/useSboms.ts` -- existing hook for fetching SBOM list; use to populate the SBOM `Select` dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- existing package table component; reference for table column definition patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` -- existing advisory list component; reference for advisory display patterns with severity
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; reuse for critical vulnerability row highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] SBOM selectors (PatternFly `Select` typeahead) load SBOM list and allow selection
- [ ] Compare button triggers API call and renders diff sections
- [ ] All six diff sections display with correct data tables and column headers matching Figma spec
- [ ] Count badges show correct item counts with appropriate colors (green, red, blue, yellow per section)
- [ ] Rows with critical severity vulnerabilities have highlighted background
- [ ] Empty state displays PatternFly `EmptyState` with `CodeBranchIcon` when no comparison performed
- [ ] Loading state shows PatternFly `Skeleton` placeholders during API call
- [ ] URL query parameters are updated on Compare click and read on page load for shareability
- [ ] Sections with >100 items use virtualized rendering

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders all six diff sections with data when comparison result is returned
- [ ] Unit test: SBOM selectors populate from `useSboms` hook data
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: URL params are read on mount and trigger comparison

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation passes
- `npx vitest run src/pages/SbomComparePage` -- component tests pass

## Dependencies
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
