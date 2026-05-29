## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` that renders the full comparison UI as specified in the Figma design. The page includes a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown, followed by six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). The page reads `left` and `right` query parameters from the URL to support bookmarkable/shareable comparisons.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section component using PatternFly ExpandableSection with Badge count and Table
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — Header toolbar component with SBOM Select dropdowns, Compare button, and Export dropdown

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to lazy-loaded SbomComparePage

## Implementation Notes
- **Figma design mapping — PatternFly components:**
  - SBOM selectors: use PatternFly `Select` component with single selection and typeahead. Populate options using the existing `useSboms` hook from `src/hooks/useSboms.ts`. Display SBOM name and version (e.g., "my-product-sbom v2.3.1").
  - Diff sections: use PatternFly `ExpandableSection` component. Each section has a title and a count `Badge`. Sections with >0 items default to expanded; sections with 0 items default to collapsed.
  - Count badge colors: Added Packages = green, Removed Packages = red, Version Changes = blue, New Vulnerabilities = red, Resolved Vulnerabilities = green, License Changes = yellow.
  - Data tables: use PatternFly composable `Table` component with sortable columns. No pagination — use virtualized rendering for sections with >100 rows (per non-functional requirement).
  - Severity indicators: use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the New Vulnerabilities and Resolved Vulnerabilities sections.
  - Empty state: use PatternFly `EmptyState` component with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
  - Loading state: use PatternFly `Skeleton` placeholders in each diff section while the API call is in progress. Disable the header toolbar during loading.
  - Export dropdown: use PatternFly `Dropdown` component with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. Export is non-MVP but the UI element should be present and disabled.
  - Compare button: PatternFly primary `Button`, disabled until both selectors have values.
- **Table columns per section (from Figma):**
  - Added Packages: Package Name, Version, License, Advisories (count)
  - Removed Packages: Package Name, Version, License, Advisories (count)
  - Version Changes: Package Name, Left Version, Right Version, Direction (upgrade/downgrade)
  - New Vulnerabilities: Advisory ID, Severity (SeverityBadge), Title, Affected Package — rows with "Critical" severity get highlighted background
  - Resolved Vulnerabilities: Advisory ID, Severity, Title, Previously Affected Package
  - License Changes: Package Name, Left License, Right License
- **URL query parameter support:** read `left` and `right` from URL search params using React Router's `useSearchParams`. When both are present on page load, auto-trigger the comparison. When the user clicks Compare, update URL search params to make the comparison shareable.
- Follow the existing page structure pattern in `src/pages/SbomListPage/SbomListPage.tsx` — page component in a directory with its own `components/` subdirectory.
- Follow the routing pattern in `src/routes.tsx` — use lazy-loaded components with React Router v6.
- Use the `useSbomComparison` hook from `src/hooks/useSbomComparison.ts` (Task 5) for data fetching.
- Use the existing `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for any full-page loading states.
- Use the existing `EmptyStateCard` from `src/components/EmptyStateCard.tsx` as reference for empty state patterns, though this page needs a custom empty state per the Figma design.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component for vulnerability severity display in New/Resolved Vulnerabilities sections
- `src/components/FilterToolbar.tsx` — existing PatternFly toolbar pattern for reference when building the comparison toolbar
- `src/components/EmptyStateCard.tsx` — existing empty state pattern for reference
- `src/components/LoadingSpinner.tsx` — existing loading indicator for full-page loading states
- `src/pages/SbomListPage/SbomListPage.tsx` — demonstrates page directory structure, PatternFly table usage, and test patterns
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — demonstrates PatternFly Table component usage with package data
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability display

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare`
- [ ] Two SBOM selector dropdowns are present and populated via the `useSboms` hook
- [ ] Compare button triggers comparison API call when both SBOMs are selected
- [ ] All six diff sections render with correct PatternFly ExpandableSection, Badge counts, and Table columns
- [ ] New Vulnerabilities rows with Critical severity have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeleton displays while comparison API call is in progress
- [ ] URL query parameters `left` and `right` are updated on comparison and read on page load
- [ ] Comparison is shareable via URL — opening a URL with both parameters auto-triggers comparison
- [ ] Export dropdown is present but disabled (non-MVP placeholder)

## Test Requirements
- [ ] Unit test: verify empty state renders when no comparison is active (no query params, no selection)
- [ ] Unit test: verify both SBOM selectors render and display SBOM options from mocked useSboms data
- [ ] Unit test: verify Compare button is disabled when only one SBOM is selected
- [ ] Unit test: verify all six diff sections render with correct titles and counts when comparison data is loaded
- [ ] Unit test: verify Critical severity rows in New Vulnerabilities section have highlighted styling
- [ ] Unit test: verify URL search params are set when Compare is clicked
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts` returning mock comparison data
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/` for test use

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add frontend API types, client function, and React Query hook

[sdlc-workflow] Description digest: sha256:1111e133d5c563b4c920cf26188faa5b3e0476890a59ecc31ed397b8e190e2b2
