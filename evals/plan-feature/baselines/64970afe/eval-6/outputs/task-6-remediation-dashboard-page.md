## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create the RemediationDashboardPage component at the `/remediation` path. The page displays summary cards showing total Open, In Progress, and Resolved vulnerability counts, plus a progress chart showing the remediation trend over the past 30 days. Summary cards use PatternFly Card components and the progress chart visualizes the trend data.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards component displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` -- progress trend chart component for 30-day remediation trend

## Implementation Notes
- Per CONVENTIONS.md $Page Structure: create a dedicated directory under `src/pages/` with the main component, test file, and `components/` subdirectory for page-specific components. Follow the pattern in `src/pages/SbomListPage/`.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's .tsx page scope.
- Per CONVENTIONS.md $Component Library: use PatternFly 5 components for all UI elements -- Card, CardTitle, CardBody for summary cards, and PageSection for page layout.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's .tsx component scope.
- Per CONVENTIONS.md $Naming: use PascalCase for component names and filenames.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's TypeScript naming scope.
- Use the `useRemediationSummary` hook from Task 5 for data fetching.
- Use the existing `LoadingSpinner` component (`src/components/LoadingSpinner.tsx`) during data loading.
- Use the existing `EmptyStateCard` component (`src/components/EmptyStateCard.tsx`) when no data is available.
- The progress chart should use a line or area chart to show the 30-day remediation trend.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` -- loading state indicator, reuse directly
- `src/components/EmptyStateCard.tsx` -- empty state placeholder when no data exists
- `src/components/SeverityBadge.tsx` -- severity level badge for labeling summary card categories
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference implementation for page structure with data fetching and loading states
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping for chart colors

## Acceptance Criteria
- [ ] Dashboard page renders at /remediation path
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Loading spinner is displayed while data is fetching
- [ ] Empty state is shown when no remediation data exists
- [ ] All components use PatternFly 5

## Test Requirements
- [ ] Verify summary cards render with correct count values from mock data
- [ ] Verify loading state is displayed during data fetch
- [ ] Verify empty state renders when API returns no data
- [ ] Verify chart component renders with trend data

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 5 -- Add remediation API types, client functions, and React Query hooks
