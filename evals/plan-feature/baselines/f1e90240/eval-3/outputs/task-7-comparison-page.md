# Task 7: Implement SBOM comparison page and components

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 6

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Build the SBOM comparison page at `/sbom/compare` following the Figma design. The page includes a header toolbar with two SBOM selector dropdowns, a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results in data tables. The page reads `left` and `right` SBOM IDs from URL query parameters to support shareable URLs.

The page must handle three states: empty (no comparison yet), loading (API call in progress), and results (diff sections rendered). For large diffs with >100 rows in a section, use virtualized lists to prevent browser freezing.

## Files to Create

- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main page component with header toolbar, state management, and diff section layout
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component wrapping PatternFly `ExpandableSection`, `Badge`, and `Table`
- `src/pages/SbomComparePage/components/SbomSelector.tsx` -- SBOM selector dropdown using PatternFly `Select` with typeahead, backed by `useSboms` hook
- `src/pages/SbomComparePage/components/ExportDropdown.tsx` -- Export dropdown with JSON and CSV options

## Acceptance Criteria

- [ ] Page renders at `/sbom/compare` with header toolbar containing two SBOM selectors, Compare button, and Export dropdown
- [ ] SBOM selectors use PatternFly `Select` (single, typeahead) populated via the existing `useSboms` hook
- [ ] Compare button is disabled until both selectors have values; triggers comparison via `useSbomComparison` hook
- [ ] URL query parameters `left` and `right` are read on page load to pre-populate selectors and auto-trigger comparison
- [ ] URL is updated (via `useSearchParams`) when a comparison is triggered, enabling shareable URLs
- [ ] Six diff sections render in order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
- [ ] Each section uses `ExpandableSection` with a `Badge` showing the item count; badge colors: green (added/resolved), red (removed/new vulns), blue (version changes), yellow (license changes)
- [ ] Sections with >0 items are expanded by default; sections with 0 items are collapsed
- [ ] Data tables in each section have sortable columns matching the Figma specification
- [ ] New Vulnerabilities section: rows with severity "Critical" have a highlighted background
- [ ] Severity values render using the existing `SeverityBadge` shared component
- [ ] Empty state (no comparison) shows PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", and descriptive body text
- [ ] Loading state shows `Skeleton` placeholders in each diff section area; toolbar is disabled during loading
- [ ] Export dropdown is disabled until comparison results are loaded

## Test Requirements

- Render test: page shows empty state when no query params are present.
- Render test: page shows loading skeletons when comparison is in progress.
- Render test: page renders all six diff sections with correct data when comparison result is provided.
- Interaction test: selecting two SBOMs and clicking Compare updates URL params and triggers the hook.
- Interaction test: clicking an ExpandableSection header toggles its expanded state.

## Implementation Notes

Create the page directory at `src/pages/SbomComparePage/` following the page structure convention. The main component manages state for selected SBOM IDs using `useSearchParams` from React Router:

```typescript
const [searchParams, setSearchParams] = useSearchParams();
const leftId = searchParams.get("left") ?? undefined;
const rightId = searchParams.get("right") ?? undefined;
```

The `DiffSection` component is a generic wrapper:

```typescript
interface DiffSectionProps<T> {
  title: string;
  badgeColor: "green" | "red" | "blue" | "yellow";
  items: T[];
  columns: TableColumn<T>[];
  isLoading: boolean;
}
```

Use PatternFly composable `Table` for data tables. For sections with >100 items, integrate `react-window` or PatternFly's built-in virtualization to satisfy the non-functional requirement for large diffs.

Reference the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for the New Vulnerabilities and Resolved Vulnerabilities sections.

### Figma Design References

- **Header Toolbar**: Two PatternFly `Select` dropdowns (single, typeahead) for SBOM selection, primary `Button` for Compare, `Dropdown` for Export (JSON/CSV options)
- **Diff Sections**: PatternFly `ExpandableSection` with `Badge` count indicators; colors per section as specified in Figma
- **Data Tables**: PatternFly composable `Table` with sortable columns; column definitions per section match Figma specifications
- **Empty State**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare"
- **Loading State**: PatternFly `Skeleton` placeholders in diff section areas
- **Critical Row Highlighting**: Rows in New Vulnerabilities with severity "Critical" get highlighted background per Figma spec

## Applicable Conventions

- **Component library** (PatternFly 5): Applies: task creates page components in `src/pages/SbomComparePage/` matching the convention's PatternFly component scope.
- **Page structure** (each page gets own directory under src/pages/): Applies: task creates `src/pages/SbomComparePage/` matching the convention's page directory scope.
- **Naming** (PascalCase for components): Applies: task creates PascalCase component files matching the convention's naming scope.
