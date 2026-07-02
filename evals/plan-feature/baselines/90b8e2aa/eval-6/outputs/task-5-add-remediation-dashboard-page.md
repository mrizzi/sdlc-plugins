## Repository
trustify-ui

## Target Branch
main

## Description
Add the remediation dashboard page at `/remediation` with three main sections: summary cards showing total Open, In Progress, and Resolved vulnerability counts; a progress chart showing remediation trend over time; and a filterable table of outstanding vulnerabilities with filters for severity, product, and status. The page uses PatternFly 5 components and consumes data from the React Query hooks created in Task 4.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component composing summary cards, progress chart, and vulnerability table
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — PatternFly Card components displaying total Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — progress chart component showing remediation trend over time (use PatternFly Charts or a lightweight charting library)
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` — filterable table component using PatternFly Table with toolbar filters for severity, product, and status

## Files to Modify
- `src/routes.tsx` — add route definition for `/remediation` path mapping to `RemediationDashboardPage` with lazy loading
- `src/App.tsx` — add navigation link for the remediation dashboard in the application nav

## Implementation Notes
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Follow the pattern established in `src/pages/SbomListPage/`.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents. Use PF5 `Card`, `CardTitle`, `CardBody` for summary cards; `Table`, `Thead`, `Tbody`, `Tr`, `Td` for the vulnerability table; `Toolbar`, `ToolbarContent`, `ToolbarItem` for filter controls.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's TypeScript component file scope.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Use `React.lazy()` and `Suspense` for the RemediationDashboardPage route definition.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript routing file scope.
- Use the `FilterToolbar` component from `src/components/FilterToolbar.tsx` for the severity/product/status filter controls instead of building custom filter UI.
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` to display severity levels in the vulnerability table.
- Use severity ordering and color mapping from `src/utils/severityUtils.ts` for consistent severity display.
- The `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` should be used for loading states.
- The `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` should be used when no remediation data is available.
- Dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation — implement client-side pagination or virtualization for the table.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — reusable filter toolbar with PatternFly; use directly for severity/product/status filters
- `src/components/SeverityBadge.tsx` — severity level badge component; reuse in the vulnerability table rows
- `src/components/EmptyStateCard.tsx` — empty state placeholder; use when no remediation data exists
- `src/components/LoadingSpinner.tsx` — loading indicator; use during data fetching
- `src/utils/severityUtils.ts` — severity ordering and color mapping; reuse for table sorting and badge colors
- `src/pages/SbomListPage/SbomListPage.tsx` — reference page implementation with table, filters, and data fetching pattern
- `src/pages/AdvisoryListPage/AdvisoryListPage.tsx` — reference page with list layout and PatternFly components

## Acceptance Criteria
- [ ] `/remediation` route is accessible and renders the dashboard page
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart renders remediation trend data
- [ ] Vulnerability table displays outstanding vulnerabilities with severity, product, and status columns
- [ ] Filter toolbar allows filtering by severity (Critical/High/Medium/Low), product, and status (Open/In Progress/Resolved)
- [ ] Selecting a product from the filter updates the dashboard to show only that product's vulnerabilities
- [ ] Table supports sorting by severity
- [ ] Loading state is shown while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Navigation includes a link to the remediation dashboard

## Test Requirements
- [ ] Verify dashboard page renders without errors when data is available
- [ ] Verify summary cards display correct aggregated counts
- [ ] Verify filter toolbar filters the vulnerability table correctly by severity
- [ ] Verify filter toolbar filters the vulnerability table correctly by product
- [ ] Verify filter toolbar filters the vulnerability table correctly by status
- [ ] Verify empty state is rendered when no data is returned
- [ ] Verify loading spinner is shown during data fetch

## Dependencies
- Depends on: Task 4 — Add remediation API types and React Query hooks
