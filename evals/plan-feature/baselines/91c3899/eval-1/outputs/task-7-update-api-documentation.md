## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error responses, and caching behavior. This enables API consumers and the frontend dashboard team to integrate with the new endpoint.

## Files to Modify
- `README.md` — Add the advisory-summary endpoint to the API endpoint listing if one exists in the README

## Implementation Notes
- Document the endpoint with the following details:
  - Path: `GET /api/v2/sbom/{id}/advisory-summary`
  - Path parameter: `id` (SBOM identifier)
  - Optional query parameter: `threshold` (values: `critical`, `high`, `medium`, `low`) — filters counts to include only severities at or above the given level
  - Success response (200): `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - Error response (404): returned when the SBOM ID does not exist
  - Caching: responses are cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM
- Follow the documentation style and format already used in `README.md` for existing endpoint descriptions.
- Note: The feature spec mentions adding the endpoint to a Grafana dashboard for latency monitoring — this is an operational concern outside the scope of this documentation task.

## Acceptance Criteria
- [ ] New endpoint is documented with path, parameters, response shape, and error responses
- [ ] Documentation mentions the caching behavior (5-minute TTL, invalidation on advisory ingestion)
- [ ] Documentation is consistent in style with existing API documentation in the repository

## Test Requirements
- [ ] Review the documentation for accuracy against the implemented endpoint behavior
- [ ] Verify all documented fields match the actual AdvisorySeveritySummary struct

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
- Depends on: Task 4 — Add endpoint caching
