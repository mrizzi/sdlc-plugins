**Summary:** Create remediation dashboard page with summary cards and progress chart
**Issue Type:** Task
**Parent Epic:** TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. Register the route in the application router with lazy loading.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component with layout, summary cards section, and progress chart section
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary card components displaying Open/In Progress/Resolved totals with severity breakdown
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — Progress chart component showing remediation trend over 30 days

## Files to Modify
- `src/routes.tsx` — Add route definition for `/remediation` pointing to lazy-loaded RemediationDashboardPage

## Implementation Notes
Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page structure scope.

Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing scope.

Use PatternFly 5 components for layout and display:
- `Card`, `CardTitle`, `CardBody` for summary cards
- `Grid`, `GridItem` for responsive dashboard layout
- `PageSection` for page structure
- Use a charting library compatible with PatternFly (e.g., PatternFly Charts or Victory) for the progress chart

The summary cards should consume the `useRemediationSummary` hook from Task 4 and display:
- Total Open count with Critical/High/Medium/Low severity breakdown
- Total In Progress count
- Total Resolved count

Reuse the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity level indicators in the summary cards.

Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` during data fetch, and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data is available.

Add the route to `src/routes.tsx` following the existing lazy-loaded route definition pattern (see how SbomListPage and AdvisoryListPage are registered).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — page structure pattern with PatternFly layout (PageSection, Grid)
- `src/components/SeverityBadge.tsx` — severity level badge component for Critical/High/Medium/Low display
- `src/components/LoadingSpinner.tsx` — loading indicator component for data fetch states
- `src/components/EmptyStateCard.tsx` — empty state placeholder component when no data exists
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] Dashboard page renders at the `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Summary cards include severity breakdown (Critical/High/Medium/Low) for open vulnerabilities
- [ ] Progress chart renders remediation trend over the past 30 days
- [ ] Page uses PatternFly 5 components consistently with existing pages
- [ ] Loading spinner displays while data is being fetched
- [ ] Empty state card displays when no remediation data is available
- [ ] Route is lazy-loaded following the established routing pattern

## Test Requirements
- [ ] Component test: summary cards display correct counts from mock remediation data
- [ ] Component test: progress chart renders without errors with valid data
- [ ] Component test: loading spinner shows while useRemediationSummary hook is in loading state
- [ ] Component test: empty state card shows when the API returns no remediation data

## Dependencies
- Depends on: Task 4 — Add remediation API client, types, and React Query hooks
