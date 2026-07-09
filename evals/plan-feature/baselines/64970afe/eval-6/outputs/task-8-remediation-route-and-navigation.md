## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Register the `/remediation` route in the application router and add a navigation entry so users can navigate to the remediation dashboard. The route should use lazy loading for the RemediationDashboardPage component, following the established routing pattern.

## Files to Modify
- `src/routes.tsx` -- add route definition for /remediation with lazy-loaded RemediationDashboardPage
- `src/App.tsx` -- add navigation entry for the remediation dashboard in the application navigation

## Implementation Notes
- Per CONVENTIONS.md $Routing: use React Router v6 with lazy-loaded page components, following the pattern in `src/routes.tsx` for existing routes like /sbom and /advisory.
  Applies: task modifies `src/routes.tsx` matching the convention's .tsx routing scope.
- Per CONVENTIONS.md $Naming: use kebab-case for the route path (`/remediation`).
  Applies: task modifies `src/routes.tsx` matching the convention's routing naming scope.
- Add a navigation link in the sidebar/nav area of App.tsx, placing it logically near security-related navigation items.
- Use React.lazy() for the RemediationDashboardPage import to enable code splitting.

## Reuse Candidates
- `src/routes.tsx` -- existing route definitions as patterns for lazy loading and path structure
- `src/App.tsx` -- existing navigation entries as reference for consistent placement and styling

## Acceptance Criteria
- [ ] Route /remediation renders the RemediationDashboardPage component
- [ ] Navigation entry is visible and links to /remediation
- [ ] Page component is lazy-loaded for code splitting
- [ ] Navigation is placed logically near security-related items

## Test Requirements
- [ ] Verify navigating to /remediation renders the dashboard page
- [ ] Verify the navigation entry is present and clickable
- [ ] Verify lazy loading does not cause errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 6 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
