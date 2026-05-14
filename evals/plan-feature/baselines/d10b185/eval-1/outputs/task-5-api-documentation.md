# Task 5 — Add API documentation for the advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint in the project's API documentation. This ensures API consumers can discover the endpoint, understand its parameters, and integrate it into dashboards and alerting systems.

## Files to Modify
- `README.md` — Add the advisory-summary endpoint to the API endpoint listing if one exists in the README

## Implementation Notes
- Review the existing `README.md` for an API reference section. If one exists, add the new endpoint following the same format used for existing endpoints like `GET /api/v2/sbom/{id}` and `GET /api/v2/advisory`.
- Document the following:
  - **Path**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Description**: Returns aggregated advisory severity counts for a given SBOM
  - **Path parameters**: `id` (UUID) — the SBOM identifier
  - **Query parameters**: `threshold` (optional, one of: `critical`, `high`, `medium`, `low`) — filter to severities at or above this level
  - **Response shape**: `{ "critical": number, "high": number, "medium": number, "low": number, "total": number }`
  - **Error responses**: 404 if SBOM not found
  - **Caching**: Response is cached for 5 minutes
- Per `docs/constraints.md` section 5.1: keep changes scoped to listed files.

## Acceptance Criteria
- [ ] The advisory-summary endpoint is documented with path, parameters, response shape, and error responses
- [ ] Documentation follows the same format as existing endpoint documentation in the project
- [ ] The `threshold` query parameter is documented with its accepted values

## Test Requirements
- [ ] Verify documentation is consistent with the actual endpoint implementation (path, parameters, response shape)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
