# Task 4: Create RemediationDashboardPage with summary cards and progress chart

**Epic**: TC-9006: trustify-ui

## Repository

trustify-ui

## Target Branch

main

## Description

Create the main remediation dashboard page at the `/remediation` route. The page displays summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trends over the past 30 days. Uses PatternFly 5 components for layout and the React Query hooks from Task 3 for data fetching.

## Acceptance Criteria

- [ ] New page directory `src/pages/RemediationDashboardPage/` created with main component
- [ ] Route `/remediation` registered in `src/routes.tsx` with lazy loading
- [ ] Summary cards display total Open, In Progress, and Resolved counts using PatternFly Card components
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Page uses `useRemediationSummary` hook for data fetching
- [ ] Loading state shows `LoadingSpinner` component
- [ ] Empty state shows `EmptyStateCard` when no data is available
- [ ] Page renders correctly with up to 10,000 tracked vulnerabilities without degradation

## Files to Modify

- `src/routes.tsx` -- add /remediation route definition with lazy-loaded component
- `src/App.tsx` -- add navigation entry for remediation dashboard

## Files to Create

- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- unit tests
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards sub-component
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- remediation trend chart component

## Implementation Notes

- Follow the page structure pattern from `src/pages/SbomListPage/`: each page has its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory
- Use PatternFly 5 `Card`, `CardTitle`, `CardBody`, `Grid`, and `GridItem` components for the summary cards layout
- Register the route in `src/routes.tsx` following the lazy-loaded pattern used by existing pages
- Reuse `src/components/LoadingSpinner.tsx` for loading states and `src/components/EmptyStateCard.tsx` for empty states
- Use `src/utils/severityUtils.ts` for severity level color mapping in the summary cards
- The progress chart can use PatternFly's charting components or a lightweight charting library already in the project

## Convention-Aware Enrichment

- **Page structure**: Applies: task creates `src/pages/RemediationDashboardPage/` matching the convention's page directory structure scope.
- **Component library**: Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's PatternFly 5 component scope.
- **Routing**: Applies: task modifies `src/routes.tsx` matching the convention's lazy-loaded route scope.
- **Shared components**: Applies: task reuses `src/components/LoadingSpinner.tsx` and `src/components/EmptyStateCard.tsx` matching the convention's shared component reuse scope.
- **Naming**: Applies: task creates `RemediationDashboardPage.tsx` matching the convention's PascalCase component naming scope.

## Reuse Candidates

- `src/components/SeverityBadge.tsx` -- severity level badge component, useful for displaying severity labels in summary cards
- `src/components/LoadingSpinner.tsx` -- loading indicator, reuse for data fetching states
- `src/components/EmptyStateCard.tsx` -- empty state placeholder, reuse when no remediation data exists
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping, reuse for chart and card colors

## Test Requirements

- Unit test: dashboard page renders summary cards with correct counts
- Unit test: loading state displays LoadingSpinner
- Unit test: empty state displays EmptyStateCard when no data
- Unit test: progress chart renders with mock trend data
