## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Register the `/remediation` route in the application router and add a navigation entry so users can access the remediation dashboard from the main navigation. The route uses lazy loading consistent with other page routes.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/remediation` pointing to `RemediationDashboardPage` with lazy loading
- `src/App.tsx` — Add navigation menu entry for the remediation dashboard in the application sidebar/nav

## Implementation Notes
Follow the routing pattern in `src/routes.tsx` where each route maps a path to a lazy-loaded page component. Reference the existing route entries for `/sbom` and `/advisory` patterns.

Per CONVENTIONS.md: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.

For `src/routes.tsx`:
- Add a new route entry: `{ path: "/remediation", element: <RemediationDashboardPage /> }`
- Use `React.lazy()` for the import to maintain code-splitting
- Place the route alongside other top-level routes

For `src/App.tsx`:
- Add a navigation item in the sidebar/header navigation matching the existing nav structure
- Use an appropriate PatternFly icon (e.g., `ShieldAltIcon` or `SecurityIcon`) for the nav entry
- Label: "Remediation" or "Remediation Dashboard"
- Position the nav item logically near security-related entries (after Advisories)

## Reuse Candidates
- `src/routes.tsx` — Existing route definitions to follow as a pattern for lazy-loading and path conventions
- `src/App.tsx` — Existing navigation structure to extend with the new entry

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the `RemediationDashboardPage`
- [ ] Navigation menu includes a "Remediation" entry that links to `/remediation`
- [ ] Route uses lazy loading for code-splitting
- [ ] Navigation entry appears in the correct position (near security-related items)
- [ ] Direct URL navigation to `/remediation` works (no 404)

## Test Requirements
- [ ] Route renders the correct page component when navigating to `/remediation`
- [ ] Navigation entry is visible in the rendered application shell

## Dependencies
- Depends on: Task 6 — Remediation dashboard page (page component must exist for route to reference)

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
