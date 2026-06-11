# Task 5 — Add SbomComparePage with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page UI at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selectors (PatternFly `Select` with typeahead), a "Compare" button, an "Export" dropdown, and six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Each section uses PatternFly `ExpandableSection` with a count `Badge` and a composable `Table`. The page supports URL-shareable comparisons via `left` and `right` query parameters.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM selector dropdown component wrapping PatternFly Select with typeahead
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` — export dropdown with JSON/CSV options

## Implementation Notes
- Follow the page directory structure: each page has its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory (see `src/pages/SbomDetailPage/` for the established pattern).
- **Figma component mapping:**
  - SBOM selectors: PatternFly `Select` (single, typeahead) — fetch SBOM list using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Pre-populate from URL query params `left` and `right`.
  - Diff sections: PatternFly `ExpandableSection` — default expanded for sections with >0 items. Title includes section name and count badge.
  - Count badges: PatternFly `Badge` — green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow for License Changes.
  - Data tables: PatternFly `Table` (composable) — sortable columns, no pagination. Use virtualized rendering for sections with >100 rows to prevent browser freezing (per non-functional requirements).
  - Severity indicators: reuse existing `SeverityBadge` component from `src/components/SeverityBadge.tsx`. Rows with severity "Critical" in the New Vulnerabilities section have a highlighted background.
  - Empty state: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` as reference.
  - Loading state: PatternFly `Skeleton` placeholders in each diff section while the comparison API call is in progress. Header toolbar disabled during loading.
  - Export dropdown: PatternFly `Dropdown` with two items "Export JSON" and "Export CSV". Disabled until comparison result is loaded. Export is non-MVP but include the dropdown shell.
  - "Compare" button: primary PatternFly `Button`, disabled until both selectors have values. Triggers the `useSbomComparison` hook refetch.
- **Table column definitions per section:**
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- URL-shareable: read `left` and `right` query params from `useSearchParams` (React Router). When both are present on page load, auto-trigger the comparison. Update URL params when user selects SBOMs and clicks Compare.
- Use `src/utils/severityUtils.ts` for severity level ordering and color mapping in the New Vulnerabilities section.
- Use `src/utils/formatDate.ts` if any date formatting is needed in the display.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge for vulnerability rows
- `src/components/EmptyStateCard.tsx` — empty state placeholder pattern
- `src/components/LoadingSpinner.tsx` — loading indicator pattern (though Skeleton is preferred per Figma)
- `src/components/FilterToolbar.tsx` — toolbar layout pattern reference
- `src/hooks/useSboms.ts` — SBOM list fetching for the selector dropdowns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — table component pattern for package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — advisory list component pattern
- `src/utils/severityUtils.ts` — severity ordering and color mapping

## Acceptance Criteria
- [ ] SbomComparePage renders with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors load the SBOM list via useSboms hook and support typeahead filtering
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare triggers the comparison API call and renders six diff sections
- [ ] Each diff section uses ExpandableSection with a count Badge in the correct color
- [ ] Diff sections with >0 items are expanded by default
- [ ] New Vulnerabilities section highlights rows with Critical severity
- [ ] Empty state shows when no comparison has been performed (no query params)
- [ ] Loading state shows Skeleton placeholders during API call
- [ ] URL encodes both SBOM IDs for bookmarking (`/sbom/compare?left={id1}&right={id2}`)
- [ ] Page auto-triggers comparison when both query params are present on load
- [ ] Export dropdown is present with JSON/CSV options (disabled until comparison loaded)

## Test Requirements
- [ ] Unit test: renders empty state when no query params are present
- [ ] Unit test: renders SBOM selectors with data from useSboms mock
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: renders diff sections with correct data after comparison API returns
- [ ] Unit test: New Vulnerabilities section shows SeverityBadge for each row
- [ ] Unit test: diff sections with 0 items are collapsed by default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook

[sdlc-workflow] Description digest: sha256-md:f9d5058c3b48febc6c0ec3b2966adaee4e37ad322ab5feb9a42390d79b2b4b2b
