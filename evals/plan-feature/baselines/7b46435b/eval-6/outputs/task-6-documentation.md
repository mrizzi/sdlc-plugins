## Repository
trustify-backend

## Target Branch
main

## Description
Document the vulnerability remediation tracking dashboard and the new aggregation API endpoints. The Feature TC-9006 Documentation Considerations indicate New Content is needed: security teams need a guide for using the remediation dashboard, and API consumers need an endpoint reference for the new remediation aggregation endpoints.

**Doc impact type**: New Content
**Details**: Security teams need a guide for using the dashboard to track remediation SLAs and prioritize fix work. API consumers need endpoint reference documentation for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`, including request parameters, response schemas, status codes, and caching behavior.

Parent Epic: TC-9006: trustify-backend

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Acceptance Criteria
- [ ] API reference documents both remediation endpoints: path, HTTP method, query parameters, response schema, status codes, and caching behavior
- [ ] Dashboard user guide explains how to navigate to `/remediation`, interpret summary cards, read the progress chart, and use severity/product/status filters
- [ ] Documentation covers use cases: viewing remediation summary (UC-1) and filtering by product (UC-2)
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the full scope identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual response schemas from `RemediationSummary` and `ProductRemediation` models
- [ ] Verify dashboard guide matches the actual UI layout, filter options, and navigation path
- [ ] Verify example API responses are valid and consistent with the implemented endpoints

## Dependencies
- Depends on: Task 3 -- Write integration tests for remediation endpoints
- Depends on: Task 5 -- Implement remediation dashboard page
