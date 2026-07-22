# Task 6: Update REST API reference documentation for advisory-summary endpoint

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Add documentation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the REST API reference. Document the endpoint path, HTTP method, path parameters, optional query parameters, response schema, status codes, caching behavior, and usage examples. This aligns with the feature's Documentation Considerations specifying "Updates -- add endpoint to REST API reference."

## Acceptance Criteria

- [ ] REST API reference includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameter (`id` as UUID), optional query parameter (`threshold`), response JSON schema, status codes (200, 404), and Cache-Control behavior
- [ ] At least one request/response example is provided showing a successful call with sample severity counts
- [ ] An example demonstrating the `?threshold=critical` query parameter is included
- [ ] Documentation is consistent in style and format with existing endpoint documentation

## Test Requirements

- [ ] Documentation renders correctly in the project's documentation system
- [ ] All example request/response payloads are valid JSON

## Dependencies

- Task 3 (advisory-summary endpoint) -- the endpoint must be implemented before documentation can accurately describe its behavior
