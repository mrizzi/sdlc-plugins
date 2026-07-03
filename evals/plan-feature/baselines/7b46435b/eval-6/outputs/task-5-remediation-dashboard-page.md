## Repository
trustify-ui

## Target Branch
main

## Description
Implement the remediation dashboard page at `/remediation` with summary cards, a progress chart showing remediation trends over time, and a filterable vulnerability table. This task creates the full dashboard UI using PatternFly 5 components, consuming the React Query hooks from Task 4 to fetch remediation data from the backend. The dashboard serves as the central view for security managers tracking remediation SLAs and engineering leads prioritizing fix work.

Parent Epic: TC-9006: trustify-ui

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component orchestrating summary cards, chart, and table
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- page component unit tests
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards displaying total Open, In Progress, and Resolved vulnerability counts using PatternFly Card components
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` -- progress chart showing remediation trend over the past 30 days
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` -- filterable table of outstanding vulnerabilities with severity, product, and status filters
- `tests/mocks/fixtures/remediation.json` -- mock remediation data for MSW handlers in tests

## Files to Modify
- `src/routes.tsx` -- add lazy-loaded route definition for `/remediation` mapping to `RemediationDashboardPage`
- `src/App.tsx` -- add navigation entry for the remediation dashboard in the app navigation
- `tests/mocks/handlers.ts` -- add MSW request handlers for remediation API endpoints

## Implementation Notes
Follow the page structure pattern from `src/pages/SbomListPage/SbomListPage.tsx`:
- Main page component in its own directory under `src/pages/`
- Page-specific sub-components in a `components/` subdirectory
- Lazy-loaded route following the React Router v6 pattern in `src/routes.tsx`

**Summary Cards (`SummaryCards.tsx`)**:
Use PatternFly `Card` components to display three key metrics:
- Total Open vulnerabilities count
- Total In Progress count
- Total Resolved count
Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity-colored indicators where appropriate. Derive totals from the `RemediationSummary` data returned by `useRemediationSummary`.

**Progress Chart (`RemediationChart.tsx`)**:
Render a trend chart showing remediation counts over the past 30 days. Use a charting library compatible with PatternFly 5. The chart should display separate lines/bars for Open, In Progress, and Resolved counts over time.

**Filterable Table (`VulnerabilityTable.tsx`)**:
Use PatternFly `Table` component with the reusable `FilterToolbar` from `src/components/FilterToolbar.tsx`. Filters include:
- Severity: Critical, High, Medium, Low (multi-select)
- Product: dropdown populated from `useRemediationByProduct` data
- Status: Open, In Progress, Resolved (multi-select)

The table must handle up to 10,000 rows with client-side pagination (per non-functional requirements). Use severity ordering and color mapping from `src/utils/severityUtils.ts`.

**Empty and Loading States**:
Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` during data fetching and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data exists.

**Route registration**: Add a lazy-loaded route in `src/routes.tsx` following the existing pattern for `SbomListPage` and `AdvisoryListPage`.

Per CONVENTIONS.md: use PatternFly 5 components for all UI elements.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md: each page gets its own directory under `src/pages/` with main component, test file, and `components/` subdirectory.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page structure scope.

Per CONVENTIONS.md: PascalCase for components, camelCase for hooks and utilities, kebab-case for directories.
Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` naming scope.

Per CONVENTIONS.md: Vitest + React Testing Library for unit tests, MSW for API mocking.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.test.tsx` testing scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- page structure pattern with table, filters, and data fetching
- `src/components/FilterToolbar.tsx` -- reusable filter toolbar with PatternFly; use directly for table filtering
- `src/components/SeverityBadge.tsx` -- severity level badge (Critical/High/Medium/Low) for table cells and cards
- `src/components/EmptyStateCard.tsx` -- empty state placeholder when no remediation data exists
- `src/components/LoadingSpinner.tsx` -- loading indicator for async data fetching states
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping for consistent severity display
- `src/utils/formatDate.ts` -- date formatting helpers for chart axis labels and table timestamps

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Vulnerability table displays columns for severity, product, status, and details
- [ ] Severity filter works to narrow table results
- [ ] Product filter works to show only selected product's vulnerabilities
- [ ] Status filter works to show only selected status's vulnerabilities
- [ ] Page handles loading state with spinner while data is fetching
- [ ] Page handles empty state gracefully when no remediation data exists
- [ ] Navigation link to `/remediation` is visible in the app navigation
- [ ] Dashboard handles up to 10,000 vulnerabilities without performance degradation

## Test Requirements
- [ ] Unit test: `RemediationDashboardPage` renders summary cards with mock data from MSW
- [ ] Unit test: `VulnerabilityTable` renders rows and supports severity filtering
- [ ] Unit test: `SummaryCards` displays correct counts from API response
- [ ] Unit test: page shows `LoadingSpinner` while data is fetching
- [ ] Unit test: page shows `EmptyStateCard` when no remediation data exists
- [ ] Unit test: filter changes trigger re-render with filtered data

## Verification Commands
- `npm run build` -- production build succeeds without errors
- `npm run test -- --filter RemediationDashboard` -- component tests pass

## Dependencies
- Depends on: Task 4 -- Create remediation API client, types, and hooks
