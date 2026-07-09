## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Document the new remediation dashboard feature and its aggregation API endpoints. The Feature's Documentation Considerations specify "New Content" with documentation for both the remediation dashboard (user guide for security teams) and the aggregation endpoints (API reference for consumers).

Doc Impact Type: New Content
Details: Security teams need a guide for using the dashboard; API consumers need endpoint reference.
Reference: Feature TC-9006 -- Add vulnerability remediation tracking dashboard.

## Acceptance Criteria
- [ ] API endpoint documentation covers GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product
- [ ] Dashboard user guide explains the summary cards, progress chart, and filterable table
- [ ] Documentation includes request/response examples for both endpoints
- [ ] Content is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API documentation matches actual endpoint behavior
- [ ] Verify dashboard user guide accurately describes the UI layout and interactions
- [ ] Verify all filter options are documented

## Dependencies
- Depends on: Task 2 -- Add remediation module with summary aggregation service and endpoint
- Depends on: Task 3 -- Add per-product remediation breakdown endpoint
- Depends on: Task 4 -- Add integration tests for remediation endpoints
- Depends on: Task 5 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 6 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 -- Register /remediation route and add navigation entry
