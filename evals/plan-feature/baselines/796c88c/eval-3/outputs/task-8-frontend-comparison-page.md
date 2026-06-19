## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the ComparisonPage component that renders the SBOM comparison UI as specified in the Figma design. This is the main user-facing page for the SBOM diff feature. It includes a header toolbar with SBOM selectors, a Compare button, and six collapsible diff sections, each with a data table and count badge. The page reads SBOM IDs from URL query parameters for shareable URLs and supports an empty state when no comparison has been performed.

## Files to Create
- `src/pages/ComparisonPage/ComparisonPage.tsx` — Main comparison page component
- `src/pages/ComparisonPage/ComparisonPage.test.tsx` — Component tests
- `src/pages/ComparisonPage/components/DiffSection.tsx` — Reusable collapsible diff section component (ExpandableSection + Table + Badge)
- `src/pages/ComparisonPage/components/SbomSelector.tsx` — SBOM selector dropdown component wrapping PatternFly Select

## Files to Modify
- `src/routes.tsx` — Add route for `/sbom/compare` pointing to `ComparisonPage`
- `src/App.tsx` — Add lazy import for ComparisonPage if needed by routing setup

## Implementation Notes

### Figma Component Mapping

The following PatternFly components map to Figma design elements:

- **SBOM selectors** (Header Toolbar): PatternFly `Select` (single, typeahead) -- fetches SBOM list via existing `useSboms` hook. Pre-populates from URL query params `left` and `right`. Each selector shows SBOM name and version (e.g., "my-product-sbom v2.3.1").
- **Compare button**: PatternFly `Button` variant="primary" -- disabled until both selectors have values. On click, updates URL query params and triggers comparison via `useSbomComparison` hook.
- **Export dropdown**: PatternFly `Dropdown` with two items ("Export JSON", "Export CSV") -- disabled until comparison result is loaded. (Export functionality is non-MVP; wire up the dropdown but leave handlers as TODO.)
- **Diff sections**: PatternFly `ExpandableSection` -- six sections in order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes. Default expanded for sections with >0 items.
- **Count badges**: PatternFly `Badge` in each section title -- color varies by section: green for Added Packages and Resolved Vulnerabilities, red for Removed Packages and New Vulnerabilities, blue for Version Changes, yellow (use `Badge` with custom color) for License Changes.
- **Data tables**: PatternFly `Table` (composable) -- sortable columns, no pagination. For >100 rows, implement virtualized rendering.
- **Severity indicator**: Existing `SeverityBadge` shared component from `src/components/SeverityBadge.tsx` -- used in the New Vulnerabilities and Resolved Vulnerabilities tables.
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." -- shown when no comparison has been performed (page load without query params).
- **Loading state**: PatternFly `Skeleton` placeholder in each diff section while the comparison API call is in progress. Header toolbar is disabled during loading.

### DiffSection Component

Create a reusable `DiffSection` component that accepts:
- `title: string` -- section title
- `count: number` -- item count for the badge
- `badgeColor: string` -- badge color variant
- `columns: TableColumn[]` -- column definitions
- `rows: any[]` -- row data
- `defaultExpanded?: boolean` -- whether to expand by default (true when count > 0)

### URL State Management

Use React Router's `useSearchParams` to read and write `left` and `right` query parameters. When the user selects SBOMs and clicks Compare, update the URL so the comparison is shareable/bookmarkable.

### Page Structure

```
ComparisonPage
├── Header Toolbar
│   ├── SbomSelector (left)
│   ├── SbomSelector (right)
│   ├── Compare Button
│   └── Export Dropdown
├── EmptyState (when no comparison performed)
├── Loading Skeleton (while fetching)
└── Diff Sections (when results loaded)
    ├── DiffSection: Added Packages (green badge)
    ├── DiffSection: Removed Packages (red badge)
    ├── DiffSection: Version Changes (blue badge)
    ├── DiffSection: New Vulnerabilities (red badge, Critical rows highlighted)
    ├── DiffSection: Resolved Vulnerabilities (green badge)
    └── DiffSection: License Changes (yellow badge)
```

For the New Vulnerabilities table, rows with severity "Critical" should have a highlighted background (use PatternFly's `isRowSelected` or custom CSS class).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Severity level badge for vulnerability tables
- `src/components/EmptyStateCard.tsx` — Empty state placeholder pattern (adapt for comparison-specific content)
- `src/components/FilterToolbar.tsx` — PatternFly toolbar pattern reference
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — Table component pattern for package data
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — Advisory list rendering pattern
- `src/hooks/useSboms.ts` — Used by SbomSelector to fetch SBOM list for dropdowns

## Acceptance Criteria
- [ ] ComparisonPage renders at `/sbom/compare` route
- [ ] Two SBOM selectors load SBOM list and allow selection
- [ ] Compare button triggers comparison API call via `useSbomComparison` hook
- [ ] URL updates with `left` and `right` query params for shareable URLs
- [ ] Page loads comparison directly when URL contains both query params
- [ ] Six diff sections render with correct PatternFly ExpandableSection, Table, and Badge components
- [ ] Badge colors match Figma spec: green (added/resolved), red (removed/new vulns), blue (version), yellow (license)
- [ ] Critical vulnerability rows have highlighted background
- [ ] Empty state renders when no comparison has been performed
- [ ] Loading skeleton renders while comparison is in progress
- [ ] SeverityBadge component is used for vulnerability severity display

## Test Requirements
- [ ] Renders empty state when no query params are present
- [ ] Renders comparison results after selecting SBOMs and clicking Compare
- [ ] Displays correct counts in section badges
- [ ] Critical vulnerability rows are visually highlighted
- [ ] URL is updated when Compare is clicked

## Dependencies
- Depends on: Task 7 — Frontend React Query hook
- Depends on: Task 6 — Frontend API types and client functions
