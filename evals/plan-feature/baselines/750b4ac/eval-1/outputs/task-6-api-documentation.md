# Task 6 — Update API documentation for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Update the project's API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error responses, and caching behavior. This ensures API consumers can discover and use the new endpoint.

## Files to Modify
- `README.md` — add documentation for the new advisory-summary endpoint in the API reference section

## Documentation Updates
- `README.md` — add a section documenting `GET /api/v2/sbom/{id}/advisory-summary` including: endpoint path, HTTP method (GET), path parameter (`id` — SBOM identifier), optional query parameter (`threshold` — severity filter: critical, high, medium, low), response shape (`{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`), 404 behavior for missing SBOMs, and 5-minute cache TTL

## Implementation Notes
- Review the existing API documentation structure in `README.md` to understand the format used for documenting other endpoints (e.g., SBOM and advisory endpoints).
- Document the following for the new endpoint:
  - **Path**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Path parameter**: `id` (string) — the SBOM identifier
  - **Query parameter**: `threshold` (optional, string) — filter to count only severities at or above this level; valid values: `critical`, `high`, `medium`, `low`
  - **Success response** (200 OK): `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
  - **Error response** (404 Not Found): returned when the SBOM ID does not exist
  - **Caching**: responses are cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM
- Place the documentation near the existing SBOM endpoint documentation for discoverability.

## Acceptance Criteria
- [ ] README.md includes documentation for `GET /api/v2/sbom/{id}/advisory-summary`
- [ ] Documentation covers: endpoint path, path parameter, optional threshold query parameter, response shape, error responses, caching behavior
- [ ] Documentation format is consistent with existing endpoint documentation in README.md

## Test Requirements
- [ ] Manual review that the documentation is accurate and matches the implemented endpoint behavior

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint and route registration
- Depends on: Task 4 — Add optional threshold query parameter to advisory-summary endpoint

[sdlc-workflow] Description digest: sha256-md:939498ad810f4563f0a7f5b6f89552f145c302532d828061c5729ab568642cc2
