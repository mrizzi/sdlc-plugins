## Repository
trustify-ui

## Description
Build the `SbomComparePage` at route `/sbom/compare`. The page renders two PatternFly `Select` dropdowns for choosing left and right SBOMs, a "Compare" primary button, and six collapsible `ExpandableSection` diff panels (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). Both SBOM IDs are encoded in URL query params (`?left={id}&right={id}`) so comparisons are bookmarkable and shareable. Critical-severity rows in the New Vulnerabilities section receive a highlighted background. Virtualized list rendering is required for sections with more than 100 rows.

## Files to Modify
- `src/routes.tsx` — add the `/sbom/compare` route pointing to the lazy-loaded `SbomComparePage` component
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection state and a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are checked

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — top-level page component; manages URL query params, calls `useSbomCompare`, and composes sub-components
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit and integration tests for the page
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — reusable PatternFly `Select` (single, typeahead) wrapper; receives SBOM list from `useSboms` and fires `onChange` with selected SBOM ID
- `src/pages/SbomComparePage/components/DiffSection.tsx` — generic PatternFly `ExpandableSection` wrapper that takes a `title`, `count`, `badgeColor`, and `children`; auto-expanded when `count > 0`
- `src/pages/SbomComparePage/components/AddedRemovedTable.tsx` — PatternFly composable `Table` for Added Packages and Removed Packages sections; columns: Package Name, Version, License, Advisories
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — PatternFly composable `Table` for Version Changes; columns: Package Name, Left Version, Right Version, Direction
- `src/pages/SbomComparePage/components/VulnerabilitiesTable.tsx` — PatternFly composable `Table` for New Vulnerabilities and Resolved Vulnerabilities; renders `SeverityBadge` in the Severity column; applies highlighted row background for `severity === "critical"`
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — PatternFly composable `Table` for License Changes; columns: Package Name, Left License, Right License

## Implementation Notes

**Route registration** — follow the lazy-load pattern in `src/routes.tsx`. Add:
```typescript
{
  path: "/sbom/compare",
  element: <Suspense fallback={<LoadingSpinner />}><SbomComparePage /></Suspense>,
  lazy: () => import("./pages/SbomComparePage/SbomComparePage"),
}
```

**URL query param management** — use React Router v6 `useSearchParams` hook to read and write `left` and `right` params. When the user changes a selector, call `setSearchParams({ left: ..., right: ... })` so the URL updates without a full navigation. Pre-populate selectors by reading `searchParams.get("left")` and `searchParams.get("right")` on mount.

**SBOM selector** — the `SbomSelector` component uses the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the PatternFly `Select` (typeahead variant) with SBOM name + version labels. The selector is disabled while `useSboms` is loading.

**Diff data flow** — call `useSbomCompare(leftId, rightId)` from `SbomComparePage.tsx` (imported from Task 2). Pass slices of `data` down to each table component as props.

**Loading state** — while `useSbomCompare` `isLoading` is true, render a PatternFly `Skeleton` inside each `DiffSection` body and disable the header toolbar. Follow the Figma spec: toolbar disabled during loading.

**Empty state** — when the page loads without both query params (i.e., no comparison performed yet), render a PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and body text "Choose an SBOM for each side and click Compare to see what changed." Follow the pattern of `src/components/EmptyStateCard.tsx`.

**PatternFly ExpandableSection** — each `DiffSection` wraps a PatternFly `ExpandableSection`. Use the `isExpanded` prop controlled by local state, defaulting to `true` when `count > 0`. Display a PatternFly `Badge` next to the section title showing the item count. Badge color classes per Figma spec:
- Added Packages: green (`pf-m-green`)
- Removed Packages: red (`pf-m-red`)
- Version Changes: blue (`pf-m-blue`)
- New Vulnerabilities: red (`pf-m-red`)
- Resolved Vulnerabilities: green (`pf-m-green`)
- License Changes: yellow (`pf-m-gold`)

**Critical vulnerability highlighting** — in `VulnerabilitiesTable.tsx`, apply PatternFly `Tr` with `className="pf-m-warning"` (or a custom CSS class `compare-row--critical`) to rows where `severity === "critical"`.

**Virtualization** — for sections with more than 100 rows, wrap the table body in a virtualized container. Use `@tanstack/react-virtual` (if already in `package.json`) or the PatternFly `VirtualizedTable` pattern. Only virtualize when `items.length > 100` to avoid overhead for small diffs.

**"Compare selected" entry point in SbomListPage** — add checkbox column to the existing PatternFly `Table` in `src/pages/SbomListPage/SbomListPage.tsx`. When exactly two rows are checked, enable a "Compare selected" toolbar button that calls `navigate(\`/sbom/compare?left=\${ids[0]}&right=\${ids[1]}\`)` using React Router's `useNavigate`.

**SeverityBadge reuse** — `VulnerabilitiesTable.tsx` must import and render the existing `src/components/SeverityBadge.tsx` component for the Severity column. Do not reimplement severity display logic.

## Reuse Candidates
- `src/hooks/useSboms.ts` — use directly to populate both `SbomSelector` dropdowns; do not duplicate the SBOM list fetch
- `src/hooks/useSbomCompare.ts` (Task 2) — the React Query hook that drives all diff data on this page
- `src/components/SeverityBadge.tsx` — render in `VulnerabilitiesTable` Severity column; handles `critical/high/medium/low` display
- `src/components/EmptyStateCard.tsx` — reference pattern for the no-comparison-yet empty state; may be used directly or referenced for PatternFly `EmptyState` structure
- `src/components/LoadingSpinner.tsx` — use as `Suspense` fallback in route definition
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar construction pattern if search/filter is added later
- `src/utils/severityUtils.ts` — severity ordering and color mapping; import if badge color logic is needed beyond the `SeverityBadge` component

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and the page renders without errors
- [ ] Both SBOM selectors pre-populate from `?left=` and `?right=` URL params on page load
- [ ] Changing a selector updates the URL query params without a full page reload
- [ ] "Compare" button is disabled until both selectors have a value
- [ ] Clicking "Compare" (or having both params present) triggers `useSbomCompare` and renders all six diff sections
- [ ] Each diff section displays the correct item count in a `Badge` with the correct color per Figma spec
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] New Vulnerabilities section renders `SeverityBadge` for each row
- [ ] Rows with `severity === "critical"` in the New Vulnerabilities section have a visually distinct highlighted background
- [ ] Loading state: `Skeleton` placeholders appear inside each section while the API call is in progress; toolbar is disabled
- [ ] Empty state: page shows `CodeBranchIcon` + "Select two SBOMs to compare" when no params are present
- [ ] `SbomListPage` shows a "Compare selected" button that is enabled only when exactly 2 SBOMs are checked
- [ ] "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Sections with >100 items render without browser freezing (virtualized list)
- [ ] TypeScript compiles with no new errors

## Test Requirements
- [ ] `SbomComparePage.test.tsx`: render with MSW returning compare fixture; assert all six section titles are visible
- [ ] Test: selectors pre-populate when URL params are present (use `MemoryRouter` with `initialEntries`)
- [ ] Test: "Compare" button disabled when one selector is empty; enabled when both have values
- [ ] Test: loading state — render `Skeleton` while MSW handler is delayed
- [ ] Test: empty state renders when no URL params present
- [ ] Test: critical-severity rows have the highlight class applied
- [ ] `SbomListPage.test.tsx` (update existing): checking two rows enables "Compare selected" button; clicking it navigates to correct URL
- [ ] E2E test (optional, `tests/e2e/sbom-compare.spec.ts`): select two SBOMs from list page, click Compare, verify diff sections appear

## Verification Commands
- `npm test -- SbomComparePage` — all page unit tests pass
- `npm run typecheck` — no TypeScript errors
- `npm run build` — production build succeeds with no bundle errors

## Dependencies
- Depends on: Task 2 — API client, models, and React Query hook for SBOM compare (`useSbomCompare` hook must exist before this page can be built)
