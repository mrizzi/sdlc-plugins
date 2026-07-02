## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Build the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trend over time. The page uses PatternFly 5 components and consumes the remediation API via the React Query hooks created in Task 5.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component with summary cards layout and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary cards component displaying total open, in-progress, and resolved counts by severity
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — Progress chart showing remediation trend over time

## Implementation Notes
Follow the page structure pattern from `src/pages/SbomListPage/SbomListPage.tsx` — each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components.

Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents. Each page gets its own directory under `src/pages/`.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md: PascalCase for components.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` and `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.

For `SummaryCards.tsx`:
- Use PatternFly `Card`, `CardTitle`, `CardBody` components
- Display three top-level cards: Open (count), In Progress (count), Resolved (count)
- Below the top-level cards, show a severity breakdown grid (Critical/High/Medium/Low rows)
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity indicators

For `RemediationChart.tsx`:
- Use a bar or stacked bar chart showing remediation progress by severity
- Use PatternFly chart components or a compatible charting library
- Handle loading and empty states appropriately

For `RemediationDashboardPage.tsx`:
- Use `useRemediationSummary()` hook to fetch data
- Show `LoadingSpinner` during loading state
- Show `EmptyStateCard` when no vulnerability data exists
- Layout: summary cards at top, chart below, with the filterable table (Task 7) area below

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Severity level badge for Critical/High/Medium/Low indicators in summary cards
- `src/components/EmptyStateCard.tsx` — Empty state placeholder for when no remediation data exists
- `src/components/LoadingSpinner.tsx` — Loading indicator during data fetch
- `src/pages/SbomListPage/SbomListPage.tsx` — Reference for page component structure and layout patterns
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping for chart colors

## Acceptance Criteria
- [ ] Dashboard page renders summary cards with Open, In Progress, and Resolved counts
- [ ] Summary cards show severity breakdown (Critical/High/Medium/Low)
- [ ] Progress chart displays remediation data visually
- [ ] Loading state shows a spinner while data is being fetched
- [ ] Empty state is displayed when no remediation data is available
- [ ] Page uses PatternFly 5 components consistently

## Test Requirements
- [ ] Component renders without crashing with mock data
- [ ] Summary cards display correct counts from mock remediation summary
- [ ] Loading state is displayed when data is loading
- [ ] Empty state is displayed when summary returns zero counts

## Dependencies
- Depends on: Task 5 — Remediation API layer (hooks and types)

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
