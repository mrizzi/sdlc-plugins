## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, path parameters, optional query parameters (threshold), response schema, status codes (200, 404), caching behavior (5-minute TTL), and usage examples for both the basic severity summary and the threshold-filtered variant.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, path parameter (SBOM ID), optional `threshold` query parameter with allowed values (critical, high, medium, low)
- [ ] Response schema is documented: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Status codes 200 (success) and 404 (SBOM not found) are documented
- [ ] Caching behavior (5-minute TTL, invalidated on advisory ingestion) is noted
- [ ] At least one usage example is provided

## Test Requirements
- [ ] Documentation renders correctly and all code examples are syntactically valid
- [ ] Endpoint path and response shape match the actual implementation

## Dependencies
- Depends on: Task 2 — Implement advisory-summary REST endpoint with caching
