**Summary:** Document remediation dashboard and aggregation endpoints
**Issue Type:** Task
**Parent Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Create documentation for the vulnerability remediation tracking dashboard feature. This covers two primary documentation needs identified in the Feature's Documentation Considerations:

1. **API endpoint reference** (for API consumers): Document the new `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints, including request parameters, response shapes, and usage examples.

2. **Dashboard user guide** (for security teams): Document how to use the remediation dashboard at `/remediation`, including the summary cards, progress chart, and filterable vulnerability table with filtering and drill-down capabilities.

**Doc impact type:** New Content
**Feature reference:** TC-9006 — Add vulnerability remediation tracking dashboard
**User purpose:** Security teams need a guide for using the dashboard; API consumers need endpoint reference.

## Acceptance Criteria
- [ ] API documentation covers both remediation endpoints with request/response examples
- [ ] Dashboard guide explains the summary cards, progress chart, and filterable table
- [ ] Documentation explains filtering by severity, product, and status
- [ ] Documentation is consistent with the implemented feature behavior
- [ ] Documentation scope covers the areas identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] Verify API endpoint documentation matches actual endpoint paths and response shapes
- [ ] Verify dashboard guide accurately describes the UI components and interactions
- [ ] Verify documentation is complete — covers all MVP requirements from the Feature description

## Dependencies
- Depends on: Task 1 — Add remediation domain model and aggregation service
- Depends on: Task 2 — Add remediation REST API endpoints
- Depends on: Task 3 — Add remediation endpoint integration tests
- Depends on: Task 4 — Add remediation API client, types, and React Query hooks
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
