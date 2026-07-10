## Repository
trustify-backend

## Target Branch
main

## Description
Add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the REST API reference documentation. The feature TC-9001 adds a severity aggregation endpoint that returns `{ critical, high, medium, low, total }` counts for a given SBOM. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`?threshold=critical|high|medium|low`), response shape, error responses (404 for non-existent SBOM), and caching behavior (5-minute cache TTL).

Doc impact type: Updates — add endpoint to REST API reference.

Reference: Feature TC-9001 (Add advisory severity aggregation endpoint) and existing SBOM advisory endpoints documentation.

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameters, query parameters, response shape, error responses, and caching behavior
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the endpoint path, parameters, and response shape as implemented
- [ ] Verify example responses match the actual API response format

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory-summary during advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
