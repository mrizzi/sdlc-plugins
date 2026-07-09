## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` following the Figma design specifications. The page includes a header toolbar with two SBOM selectors and action buttons, six collapsible diff sections with data tables, an empty state for initial page load, and loading skeleton states during API calls. URL query parameters encode both SBOM IDs for shareability. The non-MVP Export dropdown (JSON/CSV) is included in the toolbar but can be implemented as a stub initially.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component: renders the toolbar, diff sections, empty state, and loading state. Reads `left` and `right` from URL search params via React Router useSearchParams. Calls useSbomComparison hook for data.
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — Header toolbar component: two PatternFly Select (single, typeahead) dropdowns for SBOM selection pre-populated from URL params, a primary "Compare" button (disabled until both selected), and a secondary "Export" Dropdown with JSON/CSV options (disabled until comparison loaded)
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section component: PatternFly ExpandableSection with title, colored Badge count, and composable Table. Accepts columns configuration and data array. Default expanded when items > 0.

## Implementation Notes
- **Figma design — Header Toolbar:**
  - Two PatternFly `Select` components (single selection, typeahead variant) for left and right SBOM selection. Each shows SBOM name and version (e.g., "my-product-sbom v2.3.1"). Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the dropdown options.
  - Pre-populate selectors from URL query params `left` and `right` using React Router `useSearchParams`.
  - "Compare" button: PatternFly `Button` variant="primary", disabled until both selectors have values. On click, updates URL search params and triggers the comparison query.
  - "Export" dropdown: PatternFly `Dropdown` variant="secondary" with two items ("Export JSON", "Export CSV"). Disabled until comparison data is loaded. (Non-MVP: can be stubbed.)

- **Figma design — Diff Sections (six PatternFly ExpandableSection components):**
  1. **Added Packages** — PatternFly `Badge` with green color (`isRead={false}`). PatternFly composable `Table` columns: Package Name, Version, License, Advisories (count).
  2. **Removed Packages** — PatternFly `Badge` with red color (custom CSS or `--pf-v5-global--danger-color--100`). Table columns: Package Name, Version, License, Advisories (count).
  3. **Version Changes** — PatternFly `Badge` with blue color (`--pf-v5-global--info-color--100`). Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
  4. **New Vulnerabilities** — PatternFly `Badge` with red color. Table columns: Advisory ID, Severity (using existing `SeverityBadge` from `src/components/SeverityBadge.tsx`), Title, Affected Package. Rows with severity "Critical" should have a highlighted background using PatternFly `isRowSelected` or custom `--pf-v5-global--danger-color--100` background.
  5. **Resolved Vulnerabilities** — PatternFly `Badge` with green color. Table columns: Advisory ID, Severity, Title, Previously Affected Package.
  6. **License Changes** — PatternFly `Badge` with yellow/gold color (`--pf-v5-global--warning-color--100`). Table columns: Package Name, Left License, Right License.
  - Each section uses PatternFly `ExpandableSection` and is default expanded when its item count is > 0.
  - PatternFly composable `Table` with sortable columns.
  - For sections with > 100 rows: implement virtualized rendering (react-window or similar) per the NFR to prevent browser freezing.

- **Figma design — Empty State:**
  - PatternFly `EmptyState` component when no comparison has been performed (no URL params or page initial load).
  - Icon: PatternFly `CodeBranchIcon` (fallback for ComparisonIcon).
  - Title: "Select two SBOMs to compare".
  - Body: "Choose an SBOM for each side and click Compare to see what changed."
  - Reference existing `EmptyStateCard` component at `src/components/EmptyStateCard.tsx` for pattern.

- **Figma design — Loading State:**
  - PatternFly `Skeleton` placeholders in each diff section while comparison API call is in progress.
  - Header toolbar disabled during loading (disable selectors and Compare button).
  - Reference existing `LoadingSpinner` component at `src/components/LoadingSpinner.tsx` for loading patterns.

- **URL shareability:** encode both SBOM IDs in URL query params (`/sbom/compare?left={id1}&right={id2}`). When the page loads with both params, auto-trigger the comparison. Use React Router `useSearchParams` for reading and updating params.

- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope.

- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's TSX component scope.

- Use `src/utils/severityUtils.ts` for severity level ordering and color mapping when rendering the SeverityBadge in the New Vulnerabilities section.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — existing severity badge component; use directly in New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component pattern; reference for the comparison empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; reference for loading state patterns
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list; use to populate SBOM selector dropdowns
- `src/hooks/useSbomComparison.ts` — comparison hook created in Task 5; use for fetching comparison data
- `src/utils/severityUtils.ts` — existing severity ordering and color mapping; use for vulnerability display
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table column patterns and data rendering
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory rendering patterns

## Acceptance Criteria
- [ ] Comparison page renders at `/sbom/compare` with header toolbar and diff sections
- [ ] Both SBOM selectors load and display available SBOMs from the API
- [ ] Clicking "Compare" with both SBOMs selected triggers the comparison API call and renders results
- [ ] All six diff sections render with correct columns, data, and colored count badges
- [ ] Rows with Critical severity in the New Vulnerabilities section have highlighted backgrounds
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeleton appears while comparison is in progress
- [ ] URL encodes both SBOM IDs and is shareable (loading page with params auto-triggers comparison)
- [ ] Export dropdown renders with JSON and CSV options (functional or stubbed for non-MVP)
- [ ] Sections with > 100 items use virtualized rendering without browser freezing

## Test Requirements
- [ ] Test: page renders empty state when no SBOM IDs are in URL params
- [ ] Test: page renders comparison results when both SBOM IDs are provided and API returns data
- [ ] Test: loading state renders skeleton placeholders during API call
- [ ] Test: each diff section renders correct columns and data
- [ ] Test: Critical vulnerability rows have highlighted background styling
- [ ] Test: selectors pre-populate from URL query params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add TypeScript types, API client function, and React Query hook for SBOM comparison
