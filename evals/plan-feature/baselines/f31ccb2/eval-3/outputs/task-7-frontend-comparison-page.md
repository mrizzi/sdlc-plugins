# Task 7 — Create SBOM comparison page with diff sections

**Summary:** Create SBOM comparison page with header toolbar and diff sections

**Labels:** ai-generated-jira

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the main SBOM comparison page at `/sbom/compare` based on the Figma design. The page includes a header toolbar with two SBOM selectors, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, and License Changes. The page supports URL-shareable comparisons via `left` and `right` query parameters, an empty state when no comparison is loaded, and loading skeletons during API calls. For large diffs (>100 changed items), tables should use virtualized rendering.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with SBOM selectors, Compare button, Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (ExpandableSection with Badge and Table)
- `src/pages/SbomComparePage/components/AddedPackagesSection.tsx` — Added Packages diff section with table columns: Package Name, Version, License, Advisories
- `src/pages/SbomComparePage/components/RemovedPackagesSection.tsx` — Removed Packages diff section
- `src/pages/SbomComparePage/components/VersionChangesSection.tsx` — Version Changes diff section with columns: Package Name, Left Version, Right Version, Direction
- `src/pages/SbomComparePage/components/NewVulnerabilitiesSection.tsx` — New Vulnerabilities diff section with columns: Advisory ID, Severity (SeverityBadge), Title, Affected Package; critical rows highlighted
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesSection.tsx` — Resolved Vulnerabilities diff section
- `src/pages/SbomComparePage/components/LicenseChangesSection.tsx` — License Changes diff section

## Files to Modify
- `src/routes.tsx` — add route for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare`
- `tests/mocks/fixtures/sbom-comparison.json` — add mock comparison data fixture

## Implementation Notes
- **Page structure**: follow the page pattern in `src/pages/SbomDetailPage/SbomDetailPage.tsx` — each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
- **SBOM selectors**: use PatternFly `Select` (single, typeahead) populated via the existing `useSboms` hook from `src/hooks/useSboms.ts`. Pre-populate from URL query params `left` and `right` using React Router's `useSearchParams`.
- **Compare button**: PatternFly primary button, disabled until both selectors have values. On click, update URL search params and trigger the `useSbomComparison` hook.
- **Export dropdown**: PatternFly `Dropdown` with items "Export JSON" and "Export CSV". Disabled until comparison data is loaded. Export is a non-MVP feature — implement the dropdown UI but export logic can be a stub/TODO.
- **Diff sections**: use PatternFly `ExpandableSection` for each section. Include a `Badge` with count and color per the Figma design:
  - Added Packages: green badge
  - Removed Packages: red badge
  - Version Changes: blue badge
  - New Vulnerabilities: red badge
  - Resolved Vulnerabilities: green badge
  - License Changes: yellow badge
  - Sections with >0 items default to expanded; empty sections default to collapsed.
- **Data tables**: use PatternFly composable `Table` with sortable columns. No pagination — for >100 rows, implement virtualized rendering (react-window or similar).
- **New Vulnerabilities highlighting**: rows with severity "Critical" should have a highlighted background. Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the severity column.
- **Empty state**: when no comparison is loaded (no query params or initial page load), show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Follow the pattern in `src/components/EmptyStateCard.tsx`.
- **Loading state**: while the comparison API call is in progress, show PatternFly `Skeleton` placeholders in each diff section area. Disable the header toolbar during loading. Follow loading patterns from `src/components/LoadingSpinner.tsx`.
- **URL-shareable comparisons**: encode both SBOM IDs as `?left={id1}&right={id2}` query params. When the page loads with these params pre-filled, auto-trigger the comparison. This supports UC-2 (sharing comparison URLs).
- **Route registration**: add the route in `src/routes.tsx` following the existing pattern — use lazy-loaded page component.
- **Naming conventions**: PascalCase for components, camelCase for hooks/utilities, kebab-case for directories (per project conventions).

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `{ added_packages: AddedPackage[], removed_packages: RemovedPackage[], version_changes: VersionChange[], new_vulnerabilities: NewVulnerability[], resolved_vulnerabilities: ResolvedVulnerability[], license_changes: LicenseChange[] }` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- `GET /api/v2/sbom` — existing endpoint for SBOM list to populate selectors (see `modules/fundamental/src/sbom/endpoints/list.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing shared component for severity display in vulnerability tables
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern
- `src/components/LoadingSpinner.tsx` — reference for loading state pattern
- `src/components/FilterToolbar.tsx` — reference for toolbar component patterns with PatternFly
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page structure with components subdirectory
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for package data table implementation
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — reference for advisory list rendering
- `src/hooks/useSboms.ts` — existing hook to populate SBOM selectors
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for vulnerability highlighting

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` route
- [ ] Both SBOM selectors populate with available SBOMs from the existing list endpoint
- [ ] Compare button triggers API call and renders diff sections with correct data
- [ ] All six diff sections display with correct table columns and count badges
- [ ] Sections with items default to expanded; empty sections default to collapsed
- [ ] Critical vulnerability rows have highlighted background
- [ ] Empty state displays when no comparison is loaded
- [ ] Loading skeletons display while API call is in progress
- [ ] URL query params `left` and `right` are updated on compare and can be shared/bookmarked
- [ ] Page loads comparison directly when URL contains both SBOM ID params

## Test Requirements
- [ ] Unit test: page renders empty state when no query params present
- [ ] Unit test: page renders comparison results after successful API call
- [ ] Unit test: each diff section renders correct data from mock response
- [ ] Unit test: critical vulnerability rows have highlighted styling
- [ ] Unit test: Compare button is disabled when selectors are empty
- [ ] Unit test: URL params are used to pre-populate selectors
- [ ] MSW mock handler returns fixture data for comparison endpoint

## Dependencies
- Depends on: Task 6 — Add frontend API types, client function, and React Query hook for SBOM comparison
