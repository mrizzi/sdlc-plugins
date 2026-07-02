## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Create the RemediationDashboard page with PatternFly components including summary cards showing key metrics (total vulnerabilities, critical open, remediation rate), a progress chart visualizing remediation status by severity, and a filterable table listing vulnerabilities with sorting and pagination. Register the page route in the application router and add a navigation entry.

## Files to Create
- `src/pages/RemediationDashboard/RemediationDashboard.tsx` — Main dashboard page component composing summary cards, progress chart, and remediation table
- `src/pages/RemediationDashboard/components/SummaryCards.tsx` — PatternFly Card components displaying total vulnerabilities, critical open count, and overall remediation percentage
- `src/pages/RemediationDashboard/components/RemediationTable.tsx` — Filterable, sortable, paginated table of vulnerabilities with severity badges and status indicators

## Files to Modify
- `src/routes.tsx` — Add route entry for /remediation-dashboard pointing to RemediationDashboard page
- `src/App.tsx` — Add navigation entry for the remediation dashboard in the application sidebar

## Implementation Notes
Dashboard layout:
- Use PatternFly's PageSection and Grid/GridItem for responsive layout
- Top row: SummaryCards component with Card components showing key metrics
- Middle row: Progress chart using PatternFly Charts (donut or bar chart) showing remediation by severity
- Bottom row: RemediationTable with FilterToolbar integration

SummaryCards component:
- Use PatternFly Card with CardTitle and CardBody
- Display: Total Vulnerabilities, Critical Open, High Open, Remediation Rate (%)
- Data from useRemediationSummary() hook

RemediationTable component:
- Use PatternFly Table with sortable columns
- Integrate existing FilterToolbar component from `src/components/FilterToolbar.tsx`
- Integrate existing SeverityBadge component from `src/components/SeverityBadge.tsx`
- Columns: Product, Severity, Status, Open Count, Resolved Count
- Support client-side sorting and server-side pagination via useRemediationByProduct() hook

Per CONVENTIONS.md §Component Naming: use PascalCase for component files. Applies: task creates src/pages/RemediationDashboard/RemediationDashboard.tsx matching the convention's .tsx component scope.

## Acceptance Criteria
- [ ] RemediationDashboard page renders with summary cards, progress chart, and filterable table
- [ ] Summary cards display total vulnerabilities, critical open count, and remediation percentage
- [ ] Progress chart visualizes remediation status breakdown by severity
- [ ] RemediationTable supports filtering by severity, status, and product name
- [ ] RemediationTable supports column sorting and pagination
- [ ] Route /remediation-dashboard is registered and accessible
- [ ] Navigation entry appears in the application sidebar
- [ ] Page handles loading and error states gracefully with PatternFly skeleton/empty states

## Test Requirements
- [ ] RemediationDashboard renders without errors
- [ ] SummaryCards displays correct metric values from mock data
- [ ] RemediationTable renders rows and supports filter interactions

## Dependencies
- Depends on: Task 4 (React Query hooks and API types must be available)

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
